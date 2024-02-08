from setuptools import setup

setup(
    name='pdf2rm_py',
    version='0.0.1',
    packages=['pdf2rm_py'],
    url='https://github.com/Artucuno/pdf2rm-py',
    license='',
    author='Artucuno',
    author_email='artucunov@gmail.com',
    description='Convert PDFs to Remarkable Notebooks!',
    entry_points={
        "console_scripts": ['pdf2rm_py=pdf2rm_py.main:cli'],
    }
)
