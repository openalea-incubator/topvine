from __future__ import absolute_import
import openalea.plantgl.all as pgl
import os
from openalea.core.pkgmanager import PackageManager
from os.path import join
from six.moves import range


pm = PackageManager()
pkg = pm.get('alinea.topvine')
path = pkg.path


def mesh(geometry):
    #d = pgl.Tesselator()
    #geometry.apply(d)
    #return d.result
    tessel = pgl.Tesselator()
    geometry.apply(tessel)
    mesh_ = tessel.triangulation
    return mesh_

def canline(ind, label,p):
    return "p 2 %s 9 3 %s"%(str(label), ' '.join(str(x) for i in ind for x in p[i]))

class scene_to_can(object):
    """  converts a topvine scene into can file """ 

    def __init__(self):
        pass


    def __call__(self, MaScene):
        out = []
        for obj in range (len(MaScene)):
            geometry = mesh(MaScene[obj])
            label = MaScene[obj].getName()
            p = geometry.pointList
            index = geometry.indexList
            for ind in index:
                out.append(canline(ind, label,p))

        o = open(join(path, 'temp.can'), 'w')#stockage dans un fichier can temporaire
        for i in range(len(out)):
            o.write(out[i]+"\n")

        o.close()

        return join(path, 'temp.can')
        

class scene2can(object):
    """  converts a topvine scene into can file - modifier version from luztools""" 

    def __init__(self):
        pass


    def __call__(self, MaScene, name):
        out = []
        for obj in range (len(MaScene)):
            geometry = mesh(MaScene[obj])
            label = MaScene[obj].geometry.getName()
            p = geometry.pointList
            index = geometry.indexList
            for ind in index:
                out.append(canline(ind, label,p))

        o = open(join(path, name), 'w')#stockage dans un fichier can temporaire
        for i in range(len(out)):
            o.write(out[i]+"\n")

        o.close()

        return join(path, name)
        
