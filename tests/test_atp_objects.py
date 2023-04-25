import unittest
import xml.etree.ElementTree as ET

import os
import sys
sys.path.append(os.getcwd())

from atp_objects import Resistor
from atp_objects import PLS_structure
from plscadd_report import PLS_report


class Test_Resistor(unittest.TestCase):

    def setUp(self):
        self.resistor = Resistor(
            resistance = 1000,
            x_pos = 4710,
            y_pos = 4940,
            )


    def test_int_resistance(self):
        '''
        Testear que el valor de la resistencia se asignó adecuadamente.
        '''

        self.xml_element = self.resistor.create_xml_element()
        data_element = self.xml_element.find('./comp_content/data')
        self.assertEqual(data_element.get('Value'), '1000')

    def test_xml_element_has_correct_estructure(self):
        '''
        Chequea si el elemnto XML tiene dos elementos nodes y uno data.
        '''
        
        self.xml_element = self.resistor.create_xml_element()
        self.assertIsNotNone(self.xml_element)
        self.assertEqual(self.xml_element.tag, 'comp')

        node_elements = self.xml_element.findall('./comp_content/node')
        data_elements = self.xml_element.findall('./comp_content/data')
        self.assertEqual(len(node_elements), 2)
        self.assertEqual(len(data_elements), 1)


class Test_PLS_structure(unittest.TestCase):

    def setUp(self):

        self.structure1 = PLS_structure(
            name = '10',
            )


    def test_structure_coordinates(self):
        coordinates = self.structure1.get_structure_coordinates()
        real_coordinates = {
            'x': '254405.97',
            'y': '6193319.82',
            'z': '137.55',
        }
        self.assertEqual(coordinates, real_coordinates)


    def test_attachment_points(self):
        attachment_points = self.structure1.get_attachment_points()

        expected = '6193315.84'
        returned = attachment_points[1].get('insulator_attach_point').get('y')
        self.assertEqual(returned, expected)

        expected = '254406.39'
        returned = attachment_points[3].get('wire_attach_point').get('x')
        self.assertEqual(returned, expected)


if __name__ == '__main__':
    unittest.main()
