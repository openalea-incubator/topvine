""" A python tutorial for running topvine generator
"""

import matplotlib

import openalea.topvine.data_samples as data_samples
from openalea.topvine.gen_normal_canopy import gen_normal_canopy
from openalea.topvine.gen_shoot_param import gen_shoot_param
from openalea.topvine.translate_shoots import translate_shoots
from openalea.topvine.vine_topiary import VineTopiary

matplotlib.use('Qt5Agg')


# python version of topvine/macro/wralea/stand generator composite node
def _stand_generator(carto, spurs0, dspurs, f_azi, shoot):
    geom = []
    generator = gen_shoot_param()
    translator = translate_shoots()
    for v, n in carto:
        shoot_params = generator(n, spurs0, dspurs, f_azi, shoot)
        translated = translator(shoot_params, v)
        geom.append(translated)
    return geom


def main():
    # Plot file  (stand file)    --->   carto [posxyz_plant, nb_coursons]
    # For every plant, XYZ coordinates + number of shoots
    carto = data_samples.stand_file(fn='/data/carto.csv')

    # Mean shoot file (shoot file)  --->  ram_moy
    # 1st line : number of phytomers
    #  Then     : number of secondary leaves, primary leaf surface area, secondary leaf surface area
    shoot = data_samples.shoot_file(fn='/data/ex_rammoy3.csv')

    # Distribution laws for shoot parameters (dl shoot file) ---> 2W_VSP_GRE_ramd
    # X0,Y0,Z0    : distribution laws for the positioning of the spurs.
    # DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
    # Dist        : seems not to be used
    # freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
    # x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
    # S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.
    spurs0, dspurs, f_azi, shootp = data_samples.dl_shoot_file(fn='/data/2W_VSP_GRE_ramd.csv')

    # Allometry file ---> allo_Grenache
    # The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a ⋅n+b).
    allometry = data_samples.allometry_file(fn='/data/allo_Grenache.csv')

    # Distribution laws for leaf parameters (dl file)  --->  Law-leaf-2W-Grenache
    # Elevation South – Elevation North – Azimuth South – Azimuth North
    dl = data_samples.dl_file(fn='/data/Law-leaf-2W-Grenache.csv')

    geom = _stand_generator(
        carto=carto,
        spurs0=spurs0,
        dspurs=dspurs,
        f_azi=f_azi,
        shoot=shootp
    )
    generator = gen_normal_canopy()
    tab_shoot = generator(
        tab_geom=geom,
        topol=shoot,
        dl_leaf=dl
    )

    VineTopiary().generate_scene(
        tab_shoot=tab_shoot,
        dl_leaf=dl,
        allo=allometry,
        boolI=True,
        boolT=False,
        boolB=True
    )


if __name__ == '__main__':
    from IPython import get_ipython

    ip = get_ipython()
    if ip is not None:
        ip.enable_gui("qt")
        INTERACTIVE = True
    else:
        INTERACTIVE = False

    main()

    if not INTERACTIVE:
        from PyQt5.QtWidgets import QApplication

        QApplication.instance().exec_()
    pass
