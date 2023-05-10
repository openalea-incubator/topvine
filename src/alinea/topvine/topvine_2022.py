from alinea.topvine.gen_normal_canopy import gen_normal_canopy
from alinea.topvine.gen_shoot_param import gen_shoot_param
from alinea.topvine.translate_shoots import translate_shoots
from alinea.topvine.vine_topiary import vine_topiary
from alinea.topvine.write_geom_file import write_geom_file
import alinea.topvine.data_samples as ds
#%gui qt5


def topvine(stand_path='/data/carto.csv', dl_shoot_path='/data/2W_VSP_GRE_ramd.csv',
            dl_path='/data/Law-leaf-2W-Grenache.csv', shoot_path='/data/ex_rammoy3.csv',
            allom_path='/data/allo_Grenache.csv', branches=True, trunk=True, name='geom.csv', geomfile=0):
    # a function that generates all types of scenes based on diverse input

    """
    1)	Plot file  (stand file)    --->   carto

        :   For every plant, XYZ coordinates + number of shoots

    2)	Mean shoot file (shoot file)  --->  ram_moy

        :   1st line : number of phytomers
            Then     : number of secondary leaves, primary leaf surface area, secondary leaf surface area

    3)	Distribution laws for shoot parameters (dl shoot file) ---> 2W_VSP_GRE_ramd

        :   X0,Y0,Z0    : distribution laws for the positioning of the spurs.
            DX,DY,DZ    : distribution laws for the distancing of the buds in the spurs.
            Dist        : seems not to be used
            freq AZI    : frequency of shoot AZI of angle (-20, 20), (20, 160), (160, 200) and (200, 340)
            x (     )   : means of the 4 other shoot parameters, namely initial elevation, angle between basal and distal tangents (a.k.a curvature), proportion of shoot accounting for half the curvature and normalized length.
            S (    )    : Covariance matrices for the 4 other shoot parameters for each azimuth range.

    4)	Distribution laws for leaf parameters (dl file)  --->  Law-leaf-2W-Grenache

        :   Elevation South – Elevation North – Azimuth South – Azimuth North

    5)	Shoot parameter file (geom)  ---> ex_geom2

        :   For every shoot, XYZ coordinates + values of 5 parameters (Azi, Elv, Crv, Prp, Lng)

    6)	Allometry file ---> allo_Grenache

        :   The first line includes the allometric parameters a & b that link the length of a shoot with its number of phytomers (L = a ⋅n+b).

    """


    if geomfile != 0:
        geom = ds.geom_file(geomfile)
    else:
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

        # demo
        carto = ds.stand_file(stand_path)  # [posxyz_plant, nb_coursons]
        spurs0, dspurs, f_azi, shoot = ds.dl_shoot_file(dl_shoot_path)
        geom = _stand_generator(carto, spurs0, dspurs, f_azi, shoot)
        write_geom = write_geom_file()
        write_geom(geom,name)

    vt = vine_topiary()
    generator = gen_normal_canopy()
    dl = ds.dl_file(dl_path)
    allometry = ds.allometry_file(allom_path)
    shoot = ds.shoot_file(shoot_path)
    tab_shoot = generator(geom, shoot, dl)
    scene = vt(tab_shoot, dl, allometry, branches, trunk, False)   # the last parameter, "False", does nothing

    return geom
