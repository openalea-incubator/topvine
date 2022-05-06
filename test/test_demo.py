"""test generated from topvine demo wwralea"""
import alinea.topvine.data_samples as ds
from alinea.topvine.vine_topiary import vine_topiary

def test_demo_topvine_static():
    vt = vine_topiary()
    tab_shoot = ds.normal_canopy()
    allometry = ds.allometry_file()
    dl = ds.dl_file()
    scene = vt(tab_shoot, dl, allometry, False, False, False)