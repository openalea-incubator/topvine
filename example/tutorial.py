""" A python tutorial for runing topvine generator
"""

# Should be run in a qt-enabled console (ipython --gui=qt)
# otherwise use ipython %gui magic command:
# %gui qt5


from alinea.topvine.gen_normal_canopy import gen_normal_canopy
from alinea.topvine.gen_shoot_param import gen_shoot_param
from alinea.topvine.translate_shoots import translate_shoots
from alinea.topvine.vine_topiary import vine_topiary
from alinea.topvine.vine_topiary import topiary
from openalea.plantgl.all import *
from alinea.topvine.write_geom_file import write_geom_file
import alinea.topvine.data_samples as ds


# python version of topvine/macro/wralea/stand generator composite node
def _stand_generator(carto, spurs0, dspurs, f_azi, shoot):
    geom = []
    generator = gen_shoot_param()
    translator = translate_shoots()
    for v, n in carto:
        shoot_params = generator(n, spurs0, dspurs, f_azi, shoot)
        translated = translator(shoot_params, v)
        geom.append(translat000ed)
    return geom

def main():
    # Plot file  (stand file)    --->   carto [posxyz_plant, nb_coursons]
        #For every plant, XYZ coordinates + number of shoots
    stand_path='/data/carto.csv'
    # Mean shoot file (shoot file)  --->  ram_moy
        # 1st line : number of phytomers
        #  Then     : number of secondary leaves, primary leaf surface area, secondary leaf surface area
    shoot_path='/data/ex_rammoy3.csv'
    # Distribution laws for shoot parameters (dl shoot file) ---> 2W_VSP_GRE_ramd
        # X0,Y0,Z0    : distribution laws for the positioning of the spurs.
        # DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
        # Dist        : seems not to be used
        # freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
        # x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
        # S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.
    dl_shoot_path='/data/2W_VSP_GRE_ramd.csv'
    # Distribution laws for leaf parameters (dl file)  --->  Law-leaf-2W-Grenache
        # Elevation South – Elevation North – Azimuth South – Azimuth North
    dl_path='/data/Law-leaf-2W-Grenache.csv'
    # Allometry file ---> allo_Grenache
        # The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a ⋅n+b).
    allom_path='/data/allo_Grenache.csv'
    
    carto = ds.stand_file(stand_path)  # 
    spurs0, dspurs, f_azi, shootp = ds.dl_shoot_file(dl_shoot_path)
    allometry = ds.allometry_file(allom_path)
    shoot = ds.shoot_file(shoot_path)
    dl = ds.dl_file(dl_path)
    
    geom = _stand_generator(carto, spurs0, dspurs, f_azi, shootp)
    generator = gen_normal_canopy()
    tab_shoot = generator(geom, shoot, dl)
    vt = vine_topiary()
    # boolT toggles trunk visualisation
    # boolI toggles internode visualisation
    scene = vt(tab_shoot, dl, allometry, boolI=True, boolT=False, boolB=True)   # the last parameter, "False", does nothing
