"""test generated from topvine demo wwralea"""

import unittest
import openalea.topvine.data_samples as ds
from openalea.topvine.gen_normal_canopy import gen_normal_canopy
from openalea.topvine.vine_topiary import VineTopiary
from openalea.topvine.primitive import bunch
from openalea.plantgl.all import *
from openalea.topvine.reconstr_digit import visu_digit_fromcane
from openalea.topvine.topvine_2023 import topvine

class TestDemo(unittest.TestCase):
    def test_demo_topvine_static(self):
        allometry = ds.allometry_file()
        dl = ds.dl_file()
        geom = ds.geom_file()
        shoot = ds.shoot_file()

        generator = gen_normal_canopy()
        tab_shoot = generator(geom, shoot, dl)
        VineTopiary().generate_scene(tab_shoot, dl, allometry, False, False, False)

    def test_demo_stand_generator(self):
        geom = topvine()
        self.assertIsNotNone(geom)

    def test_demo_bunch(self):
        MaScene = bunch(Scene(), [0, 0, 0], opt="s", id_='200000000000')
        MonViewer = Viewer
        MonViewer.display(MaScene)

    def test_demo_digitcane_compact(self):
        carto = ds.stand_file('/data/carto_CL.csv')
        topo = ds.shoot_file('/data/ram_moy_CL.csv')
        dazi = [90.0, 30.0]
        dincli = [45, 20.0]
        par_allo = [0.14330999999999999, 2.7161, -0.74456]
        digit_data = ds.digit_file('/data/digitCollectionMtp10_rideau_simple.csv')
        MaScene = visu_digit_fromcane.visu_digit_fromcane(digit_data, carto, topo, dazi, dincli, par_allo)[0]
        MonViewer = Viewer
        MonViewer.display(MaScene)

if __name__ == '__main__':
    unittest.main()