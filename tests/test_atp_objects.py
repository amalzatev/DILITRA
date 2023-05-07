import unittest
from unittest.mock import Mock

import os
import sys

sys.path.append(os.getcwd())

from atp_objects import Resistor
from atp_objects import PLS_structure
from atp_objects import LCC


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

    def test_ahead_span(self):
        expected_span = 435.48
        self.assertEqual(self.structure1.ahead_span, expected_span)

    def test_structure_coordinates(self):
        coordinates = self.structure1.coordinates
        real_coordinates = {
            'x': 254405.97,
            'y': 6193319.82,
            'z': 137.55,
        }
        self.assertEqual(coordinates, real_coordinates)

    def test_attachment_point(self):

        returned = self.structure1.get_attachment_point(
            set_no='2',
            phase_no='1',
            point='wire_attach_point_y'
        )
        self.assertEqual(returned, 6193315.84)

        returned = self.structure1.get_attachment_point(
            set_no='1',
            phase_no='1',
            point='wire_attach_point_z'
        )
        self.assertEqual(returned, 174.05)

        returned = self.structure1.get_attachment_point(
            set_no='2',
            phase_no='1',
            point='set_label'
        )
        self.assertRaises(ValueError)

    def test_get_structure_sets(self):
        self.assertEqual(self.structure1.sets, ['1', '2'])

    def test_get_structure_phases(self):
        phases = {
            '1': ['1'],
            '2': ['1', '2', '3'],
        }
        self.assertEqual(self.structure1.phases, phases)


class Test_LCC(unittest.TestCase):

    def setUp(self):

        self.structure = Mock()
        self.structure.sets = ['1', '2']

        self.lcc = LCC(
            id = 'lcc',
            length = 1.0,
            frequency = 60.0,
            grnd_resist = 100.0,
            structure = self.structure,
        )

    def test_get_num_circuits(self):

        self.assertEqual(self.lcc.get_num_circuits(), 1)

        self.lcc.structure.sets = ['1', '2', '3']
        self.assertEqual(self.lcc.get_num_circuits(), 2)

        self.lcc.structure.sets = ['1', '10', '11', '12']
        self.assertEqual(self.lcc.get_num_circuits(), 0)


if __name__ == '__main__':
    unittest.main()
