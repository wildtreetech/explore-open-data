"""
Usage: python clean_notebook.py notebook.ipynb [ > without_output.ipynb ]
Modified from https://gist.github.com/damianavila/5305869
Modified from remove_output by Minrk
"""
import sys
import io
from nbformat.current import read, write


def remove_outputs(nb):
    """remove the outputs from a notebook"""
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == 'code':
                cell.outputs = []

if __name__ == '__main__':
    fname = sys.argv[1]
    with io.open(fname, 'r') as f:
        nb = read(f, 'json')

    remove_outputs(nb)

    write(nb, sys.stdout, 'json')
