from __future__ import absolute_import

from alinea.topvine.topiary import topiary
from .primitive import trunk
from six.moves import range
from openalea.plantgl.all import Viewer, Scene


class vine_topiary(object):
    """  Generates a scaled PGL scene from a list of normalised shoot objects """ 

    def __init__(self):
        pass


    def __call__(self, tab_shoot,  dl_leaf, allo, boolI, boolT, boolB):
        MaScene = Scene()
        geometry = []
        labels = []
        MonViewer = Viewer
        for i in range(len(tab_shoot)):
            coord = tab_shoot[i][0].geom[1]
            for j in range(len(tab_shoot[i])):
                coord = (coord + tab_shoot[i][j].geom[1])/2
                geoms, labs = topiary(tab_shoot[i][j], allo, dl_leaf, visu_en = boolI)
                geometry.extend(geoms)
                labels.extend(labs)
                for g in geoms:
                    MaScene.add(g)

            # add a trunk if option is set to True
            if boolT == True:
                trunk(MaScene, coord/100., 'cordon')

            # a ameliorer: / type / calcul plus precis des rangs sur moy plus larges ou sur donnees filees en entree
        #TODO : generate mtg from labs and geometry
        MonViewer.display(MaScene)
        return MaScene, geometry, labels