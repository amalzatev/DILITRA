import os
import sys

sys.path.append(os.getcwd())

import unittest
import numpy as np

import utils

class Test_utils(unittest.TestCase):

    def test_calculate_vector(self):

        vector = utils.calculate_vector(
            point1 = np.array([1.0, 5.3]),
            point2 = np.array([10.3, -6.7]),
        )
        expected = np.array([9.3, -12.0])
        self.assertTrue(np.array_equal(expected, vector))

        vector = utils.calculate_vector(
            point1 = np.array([5, -9]),
            point2 = np.array([-6, -7]),
        )
        expected = np.array([-11.0, 2.0])
        self.assertTrue(np.array_equal(expected, vector))
    
    def test_calculate_angle_two_vector(self):

        self.assertAlmostEqual(
            
            utils.calculate_angle_two_vector(
                np.array([0.682, -0.732]),
                np.array([1.000, 0.008]),
            ),
            0.829,
            3,
        )

        self.assertAlmostEqual(
            
            utils.calculate_angle_two_vector(
                np.array([14.687, 9.140]),
                np.array([-6.236, 1.478]),
            ),
            2.352,
            3,
        )


    def test_calculate_unit_vector(self):

        np.testing.assert_almost_equal(
            utils.calculate_unit_vector(np.array([53.124, -41.312])),
            np.array([0.789, -0.614]),
            3,
        )

        np.testing.assert_almost_equal(
            utils.calculate_unit_vector(np.array([251631.03, 6192607.43])),
            np.array([0.041, 0.999]),
            3,
        )



if __name__ == '__main__':
    unittest.main()

