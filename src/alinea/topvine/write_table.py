from __future__ import absolute_import
from . import IOtable
from os.path import join

def write_table(table, path, name):
    p = join(path, name)
    out = open(p, 'w')
    IOtable.ecriture_csv (table, out)  
    out.close()
    return p
