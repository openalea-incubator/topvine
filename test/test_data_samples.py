import unittest
import alinea.topvine.data_samples as ds

class TestDataSamples(unittest.TestCase):
    def test_readers(self):
        geom = ds.geom_file()
        shoot = ds.shoot_file()
        d1 = ds.dl_file()
        allometry = ds.allometry_file()

    def test_normal_canopy(self):
        can = ds.normal_canopy()

if __name__ == '__main__':
    unittest.main()