"""
Usage: python clean_notebook.py notebook.ipynb
Overwrites the notebook with a version without outputs
Modified from https://gist.github.com/damianavila/5305869
Modified from remove_output by Minrk
"""
import sys
import io
import nbformat
from nbformat import read, write


def remove_outputs(nb):
    """remove the outputs from a notebook"""
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.outputs = []

if __name__ == '__main__':
    fname = sys.argv[1]
    with io.open(fname, 'r') as f:
        nb = read(f, as_version=nbformat.NO_CONVERT)

    remove_outputs(nb)

    with io.open(fname, 'w') as f:
        write(nb, f, version=nbformat.NO_CONVERT)
