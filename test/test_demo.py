"""test generated from topvine demo wwralea"""
import alinea.topvine.data_samples as ds
from alinea.topvine.gen_normal_canopy import gen_normal_canopy
from alinea.topvine.vine_topiary import vine_topiary
from alinea.topvine.gen_shoot_param import gen_shoot_param
from alinea.topvine.translate_shoots import translate_shoots


def test_demo_topvine_static():
    vt = vine_topiary()
    allometry = ds.allometry_file()
    dl = ds.dl_file()
    geom = ds.geom_file()
    shoot = ds.shoot_file()
    
    generator = gen_normal_canopy()
    tab_shoot = generator(geom, shoot, dl) 
    scene = vt(tab_shoot, dl, allometry, False, False, False)

def test_demo_stand_generator():

    # python version of topvine/macro/wralea/stand generator composite node
    def _stand_generator(carto, spurs0, dspurs, f_azi, shoot):
        geom = []
        generator = gen_shoot_param()
        translator = translate_shoots()
        for v,n in carto:
            shoot_params = generator(n, spurs0, dspurs, f_azi, shoot)
            translated = translator(shoot_params, v)
            geom.append(translated)
        return geom

    # demo
    carto = ds.stand_file()
    spurs0, dspurs, f_azi, shoot = ds.dl_shoot_file()
    geom = _stand_generator(carto, spurs0, dspurs, f_azi, shoot)
    #write_geom(geom)
    # TODO: test if this geom file is the same as the one used in test_demo_topvine_static ?
    
    # here we continue with demo_fspm10_compact :
    vt = vine_topiary()
    generator = gen_normal_canopy()
    dl = ds.dl_file()
    allometry = ds.allometry_file()
    shoot = ds.shoot_file()
    tab_shoot = generator(geom, shoot, dl)
    scene = vt(tab_shoot, dl, allometry, False, False, False)
    
    return geom