"""test generated from topvine demo wwralea"""

import alinea.topvine.data_samples as ds
from alinea.topvine.gen_normal_canopy import gen_normal_canopy
from alinea.topvine.vine_topiary import vine_topiary
from alinea.topvine.primitive import bunch
from openalea.plantgl.all import *
from alinea.topvine.reconstr_digit import visu_digit_fromcane

from alinea.topvine.topvine_2022 import topvine

def test_demo_topvine_static():
    vt = vine_topiary()
    allometry = ds.allometry_file()
    dl = ds.dl_file()
    geom = ds.geom_file()
    shoot = ds.shoot_file()
    
    generator = gen_normal_canopy()
    tab_shoot = generator(geom, shoot, dl) 
    scene, geometry, labels = vt(tab_shoot, dl, allometry, False, False, False)

def test_demo_stand_generator():


    geom, geometry, labels = topvine()

    return geom, geometry, labels


def test_demo_bunch():
    MaScene = bunch(Scene(), [0, 0, 0], opt="s", id_='200000000000')
    MonViewer = Viewer
    MonViewer.display(MaScene)

def test_demo_digitcane_compact():   #ça manque le parti caribou bien sûr
    carto = ds.stand_file('/data/carto_CL.csv')
    topo = ds.shoot_file('/data/ram_moy_CL.csv')
    dazi = [90.0, 30.0]
    dincli = [45, 20.0]
    par_allo = [0.14330999999999999, 2.7161, -0.74456]
    digit_data = ds.digit_file('/data/digitCollectionMtp10_rideau_simple.csv')
    MaScene = visu_digit_fromcane.visu_digit_fromcane(digit_data, carto, topo, dazi, dincli, par_allo)[0]
    MonViewer = Viewer
    MonViewer.display(MaScene)