"""test generated from topvine demo wwralea"""
import alinea.topvine.data_samples as ds
from alinea.topvine.stand_generator import stand_generator
from alinea.topvine.vine_topiary import vine_topiary
from alinea.topvine.write_geom_file import write_geom_file


def test_demo_topvine_static():
    vt = vine_topiary()
    tab_shoot = ds.normal_canopy()
    allometry = ds.allometry_file()
    dl = ds.dl_file()
    scene = vt(tab_shoot, dl, allometry, False, False, False)

def test_demo_stand_generator():
    carto = read_stand_file(r'./src/alinea/topvine/carto/carto.csv')
    tabgeom = stand_generator(, CxT, personalise, nbr, nbp)
    write_geom_file(tabgeom,"test_generated_stand.csv")