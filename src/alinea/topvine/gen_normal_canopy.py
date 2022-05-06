import numpy
import random
import leaf
import shoot


class gen_normal_canopy(object):
    """  generates a list of normalised shoot objects associationg average topology with geometric features (primary shoot geom, leaf angles, leaf dimensions) """ 

    def __init__(self):
        pass


    def __call__(self, tab_geom, topol, dl_leaf):
        res = []
        for i in range(len(tab_geom)):
            p = []
            for j in range(len(tab_geom[i])):
                p.append(shoot.Shoot(tab_geom[i][j], topol, dl_leaf))

            res.append(p)

        return res

