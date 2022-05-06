from __future__ import absolute_import
from . import IOtable
import numpy
from six.moves import map
from six.moves import range

class read_geom_file(object):
    """  read geom file and return shoot params as a table """ 

    def __init__(self):
        pass


    def __call__(self, path_geom):
        f = open(path_geom, 'r')
        tab_geom = IOtable.table_csv_str(f) 
        f.close()

        res = []
        for i in range(len(tab_geom)):
            tab_geom[i] = list(map(float, tab_geom[i]))
            tab_geom[i]=[int(tab_geom[i][0])]+[numpy.array(tab_geom[i][1:4])]+tab_geom[i][4:]

            if i==0: #1ere plante
                p = []

            if i>=1: #changement de plante
                if (tab_geom[i][0]-tab_geom[i-1][0])<-2 and tab_geom[i-1][0]!=7:
                    res.append(p)
                    p = []

            p.append(tab_geom[i])

            if i==len(tab_geom)-1: #derniere plante
                res.append(p)

        return res
