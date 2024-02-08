import json
import time
import os
import sys
import subprocess
import uuid
import shutil
import zipfile
import argparse
from pathlib import Path

temp_dir = "temp"

parser = argparse.ArgumentParser()
parser.add_argument("-q", action="store_true", help="Less messages to stdout (quiet)")
parser.add_argument("-s", type=float, default=0.75, help="SCALE value. Def=0.75")
parser.add_argument("-v", action="store_true", help="More messages to stdout (verbose)")
parser.add_argument("file", help="file.pdf")

n_metadata = {
    "deleted": False,
    "lastModified": f"{int(time.time())}",
    "lastOpened": f"{int(time.time())}",
    "lastOpenedPage": 0,
    "metadatamodified": False,
    "modified": False,
    "parent": "",
    "pinned": False,
    "synced": False,
    "type": "DocumentType",
    "version": 1,
    "visibleName": "Notebook"
}

content_data = {
    "coverPageNumber": -1,
    "dummyDocument": False,
    "extraMetadata": {
        "LastBallpointColor": "Black",
        "LastBallpointSize": "2",
        "LastBallpointv2Color": "Black",
        "LastBallpointv2Size": "2",
        "LastCalligraphyColor": "Black",
        "LastCalligraphySize": "2",
        "LastClearPageColor": "Black",
        "LastClearPageSize": "2",
        "LastEraseSectionColor": "Black",
        "LastEraseSectionSize": "2",
        "LastEraserColor": "Black",
        "LastEraserSize": "2",
        "LastEraserTool": "Eraser",
        "LastFinelinerColor": "Black",
        "LastFinelinerSize": "2",
        "LastFinelinerv2Color": "Black",
        "LastFinelinerv2Size": "2",
        "LastHighlighterColor": "Black",
        "LastHighlighterSize": "2",
        "LastHighlighterv2Color": "Black",
        "LastHighlighterv2Size": "2",
        "LastMarkerColor": "Black",
        "LastMarkerSize": "2",
        "LastMarkerv2Color": "Black",
        "LastMarkerv2Size": "2",
        "LastPaintbrushColor": "Black",
        "LastPaintbrushSize": "2",
        "LastPaintbrushv2Color": "Black",
        "LastPaintbrushv2Size": "2",
        "LastPen": "SharpPencilv2",
        "LastPencilColor": "Black",
        "LastPencilSize": "2",
        "LastPencilv2Color": "Black",
        "LastPencilv2Size": "2",
        "LastReservedPenColor": "Black",
        "LastReservedPenSize": "2",
        "LastSelectionToolColor": "Black",
        "LastSelectionToolSize": "2",
        "LastSharpPencilColor": "Black",
        "LastSharpPencilSize": "2",
        "LastSharpPencilv2Color": "Black",
        "LastSharpPencilv2Size": "2",
        "LastSolidPenColor": "Black",
        "LastSolidPenSize": "2",
        "LastTool": "SharpPencilv2",
        "LastUndefinedColor": "Black",
        "LastUndefinedSize": "1",
        "LastZoomToolColor": "Black",
        "LastZoomToolSize": "2"
    },
    "fileType": "notebook",
    "fontName": "",
    "lineHeight": -1,
    "margins": 100,
    "orientation": "portrait",
    "pageCount": "",
    "pages": [],
    "textAlignment": "left",
    "textScale": 1,
    "transform": {
        "m11": 1,
        "m12": 0,
        "m13": 0,
        "m21": 0,
        "m22": 1,
        "m23": 0,
        "m31": 0,
        "m32": 0,
        "m33": 1
    }
}

metadata_data = {
    "layers": [
        {
            "name": "Layer 1"
        }
    ]
}


def cleanup(temp_dir):
    print("Cleaning up...")
    shutil.rmtree(temp_dir)


def main(file, **kwargs):
    QVFLAG = "-q" if kwargs.get('q') else ""
    VERBOSE = True if kwargs.get('v') else False
    SCALE = kwargs.get('s') if kwargs.get('s') else 0.75

    page_hcl_path = os.path.join(temp_dir, "page.hcl")
    os.makedirs(temp_dir, exist_ok=True)
    with open(page_hcl_path, "w+") as page_hcl:
        page_hcl.write("""pen black 0.1 solid
line 1 1 156 1
line 156 1 156 208
line 156 208 1 208
line 1 208 1 1
moveto 0 0
""")

    NB = os.path.join(temp_dir, "Notebook")
    os.makedirs(NB, exist_ok=True)

    _page = 0
    UUID_N = str(uuid.uuid4())
    os.makedirs(os.path.join(NB, UUID_N), exist_ok=True)

    if VERBOSE:
        print(f"Working on file: {file}")
    if not os.path.isfile(file):
        print(f"{file}: No such file or directory.")
        parser.print_help()
        sys.exit(1)

    FILETYPE = None
    if Path(file).suffix.lower() in (".jpg", ".jpeg"):
        FILETYPE = "image/jpeg"
    elif Path(file).suffix.lower() == ".png":
        FILETYPE = "image/png"
    elif Path(file).suffix.lower() == ".pdf":
        FILETYPE = "application/pdf"
    else:
        print("Unsupported file type:", Path(file).suffix)
        sys.exit(1)

    if FILETYPE == "image/jpeg" or FILETYPE == "image/png":
        _NP = 1
    elif FILETYPE == "application/pdf":
        _NPa = subprocess.run(["pdfinfo", file], capture_output=True, text=True).stdout.split()
        _NP = None
        for f in _NPa:
            if f == "Pages:":
                _NP = int(_NPa[_NPa.index(f) + 1])
                break
        print(_NP)
        if not _NP:
            print("Error: Could not determine number of pages in PDF.")
            sys.exit(1)
    else:
        print("Unsupported file type:", FILETYPE)
        sys.exit(1)

    _PP = 1
    while _PP <= _NP:
        shutil.copyfile(page_hcl_path, os.path.join(temp_dir, f"P_{_page}.hcl"))

        if FILETYPE == "image/jpeg" or FILETYPE == "image/png":
            with open(os.path.join(temp_dir, f"P_{_page}.hcl"), "a") as hcl_file:
                hcl_file.write(f"moveto 12 12\n")
                hcl_file.write(f"image {{{file}}} 200 0 0 {SCALE}\n")
        elif FILETYPE == "application/pdf":
            with open(os.path.join(temp_dir, f"P_{_page}.hcl"), "a") as hcl_file:
                hcl_file.write(f"image {{{file}}} {_PP} 0 0 {SCALE}\n")

        UUID_P = str(uuid.uuid4())
        pdir = os.path.join(NB, UUID_N, f"{UUID_P}.rm")
        print(f"Processing page {_PP} of {_NP} from {file} as {UUID_P} ({pdir})")
        a = ["java", "-jar", "drawj2d.jar"]
        if QVFLAG:
            a.append(QVFLAG)
        a.extend(["-T", "rm", "-o", pdir, os.path.join(temp_dir, f"P_{_page}.hcl")])
        subprocess.run(a)
        with open(os.path.join(NB, f"{UUID_N}/{UUID_P}-metadata.json"), "w") as metadata_file:
            json.dump(metadata_data, metadata_file, indent=4)

        content_data["pages"].append(UUID_P)

        _PP += 1
        _page += 1

    content_data["pageCount"] = _page

    with open(os.path.join(NB, f"{UUID_N}.content"), "w+") as content_file:
        json.dump(content_data, content_file, indent=4)

    with open(os.path.join(NB, f"{UUID_N}.pagedata"), "w+") as pagedata_file:
        pagedata_file.write("Blank")

    n_metadata["visibleName"] = f"{Path(file).stem}"

    with open(os.path.join(NB, f"{UUID_N}.metadata"), "w+") as nmd_file:
        json.dump(n_metadata, nmd_file, indent=4)

    with zipfile.ZipFile(os.path.join(NB, "Notebook.zip"), "w") as zipf:
        for f in os.listdir(os.path.join(NB, UUID_N)):
            # Write the file to the zip file with the same name as the file
            if os.path.isfile(os.path.join(NB, UUID_N, f)):
                zipf.write(os.path.join(NB, UUID_N, f), arcname=os.path.join(UUID_N, f))

        for f in os.listdir(NB):
            if f != "Notebook.zip" and os.path.isfile(os.path.join(NB, f)):
                zipf.write(os.path.join(NB, f), arcname=f)

    shutil.copyfile(os.path.join(temp_dir, "Notebook", "Notebook.zip"), "Notebook.zip")
    print("Output written to Notebook.zip")

    cleanup(temp_dir)


def cli():
    args = parser.parse_args()
    kw = {"q": args.q, "s": args.s, "v": args.v}
    main(args.file, **kw)
