from __future__ import absolute_import
from . import IOtable
import os
from os.path import join
from openalea.core.pkgmanager import PackageManager
from six.moves import range

pm = PackageManager()
pkg = pm.get('alinea.topvine') 
path = pkg.path 

class write_geom_file(object):
    """  save shoot params in a csv file """ 

    def __init__(self):
        pass


    def __call__(self, tab_geom, name):
        #mise a plat du tableau 3 dim
        res = []
        for p in range(len(tab_geom)):
            for ram in range(len(tab_geom[p])):
                a = [tab_geom[p][ram][0]] + tab_geom[p][ram][1].tolist() + tab_geom[p][ram][2:]
                res.append(a)

        #ecriture du fichier
        out = open(join(path, name), 'w')
        IOtable.ecriture_csv (res, out)  
        out.close()

        return join(path, name)
