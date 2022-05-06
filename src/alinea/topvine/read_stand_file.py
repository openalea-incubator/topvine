from __future__ import absolute_import
from . import IOtable
from numpy import array
from six.moves import range


class read_stand_file(object):
    """  get stand caracteristics from csv stand file """ 

    def __init__(self):
        pass


    def __call__(self, path):
        f = open(path)
        tab = IOtable.table_csv_str(f)
        f.close()

        for i in range(len(tab)): #[array(x,y,z), n]
            tab[i] = [array([float(tab[i][0]), float(tab[i][1]), float(tab[i][2])]), int(tab[i][3])]
            

        return tab
