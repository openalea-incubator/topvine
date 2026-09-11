import unittest

from topvine.generate_rameau_moyen import set_profile_primary_leaf_area


class TestSetProfilePrimaryLeafArea(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rank_internode_at_max_leaf_area = 10
        cls.fraction_initial_to_max_leaf_area = 0.306
        cls.nb_primary_internodes = 24
        cls.leaf_area_max = 1

        cls.leaf_area_profile: list[float] = set_profile_primary_leaf_area(
            rank_internode_at_max_leaf_area=cls.rank_internode_at_max_leaf_area,
            fraction_initial_to_max_leaf_area=cls.fraction_initial_to_max_leaf_area,
            nb_primary_internodes=cls.nb_primary_internodes,
            leaf_area_max=cls.leaf_area_max,
        )

    def test_initial_value(self):
        self.assertEqual(
            self.leaf_area_profile[0],
            self.fraction_initial_to_max_leaf_area * self.leaf_area_max,
        )

    def test_max_value(self):
        self.assertEqual(
            self.leaf_area_profile[self.rank_internode_at_max_leaf_area - 1],
            self.leaf_area_max,
        )

    def test_end_value_is_not_zero(self):
        self.assertGreater(
            self.leaf_area_profile[-1],
            0,
        )


if __name__ == '__main__':
    unittest.main()
