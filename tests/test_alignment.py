import os
import sys
sys.path.append(os.getcwd())

import unittest
from unittest.mock import Mock

class TestAlignment(unittest.TestCase):
    def setUp(self):

        print("SetUp")

        names = ['1', '2', '3', '4']
        coordinates = [
            {
                'x': 51.1842,
                'y': 77.9259,
            },
            {
                'x': 72.3116,
                'y': 93.9350,
            },
            {
                'x': 85.8941,
                'y': 79.6190,
            },
            {
                'x': 80.0406,
                'y': 63.2118,
            },
        ]

        structures = []
        for name, i_coordinates in zip(names, coordinates):
            structure = Mock()
            structure.name = name
            structure.coordinates = i_coordinates
            structures.append(structure)
        
        for structure in structures:
            print(structure.name, structure.coordinates.get('x'), structure.coordinates.get('y'))

        def test_alignment
        

if __name__ == '__main__':
    unittest.main()
