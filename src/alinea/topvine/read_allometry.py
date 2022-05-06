from __future__ import absolute_import
from . import IOtable

class read_allometry(object):
    """  set L-N allometric parameters from alometry file """ 
    def __init__(self):
        pass

    def __call__(self, f_allo):
        f = open(f_allo, 'r')
        tab = IOtable.table_csv(f) #a remplacer part d3d / utiliser IOtable.table_txt
        f.close()

        return tab
