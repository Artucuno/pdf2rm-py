# pdf2rm-py
[![rm1](https://img.shields.io/badge/rM1-supported-green)](https://remarkable.com/store/remarkable)
[![rm2](https://img.shields.io/badge/rM2-supported-green)](https://remarkable.com/store/remarkable-2)
[![Discord](https://img.shields.io/discord/385916768696139794.svg?label=reMarkable&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/ATqQGfu)

Convert PDFs to Remarkable Notebooks!

## Prerequisites
- [pdfinfo](https://www.xpdfreader.com/download.html) (part of Xpdf)
- [drawj2d](https://sourceforge.net/projects/drawj2d/files/latest/download?source=files)

## Installation
```bash
git clone https://github.com/Artucuno/pdf2rm-py.git
cd pdf2rm-py
python setup.py install
```

## Usage
This script becomes a command line tool after installation. The following command will convert `input.pdf` to `Notebook.zip`:
```bash
pdf2rm_py [-h] [-q] [-s S] [-v] file
```
```
options:
  -h, --help  show this help message and exit
  -q          Less messages to stdout (quiet)
  -s S        SCALE value. Def=0.75
  -v          More messages to stdout (verbose)
```

## Credits <3
- [JCN-9000/pdf2rmnotebook](https://github.com/JCN-9000/pdf2rmnotebook)
- [naturale0](https://gist.github.com/naturale0/89026143415719ca0a1bab1e708ba0a4)\
