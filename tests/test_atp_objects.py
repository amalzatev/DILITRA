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

    def test_get_num_phases(self):

        self.assertEqual(self.lcc.get_num_phases(), 2)

        self.lcc.structure.sets = ['1', '2', '3']
        self.assertEqual(self.lcc.get_num_phases(), 3)

        self.lcc.structure.sets = ['1', '10', '11', '12']
        self.assertEqual(self.lcc.get_num_phases(), 4)

    def test_calculate_horiz(self):

        # Primera prueba
        self.structure.coordinates = {
            'x': 99.2666,
            'y': 212.3338,
        }
        self.structure.sets = ['1']
        self.structure.phases = {
            '1': ['1', '2'],
        }

        next_structure = Mock()
        next_structure.coordinates = {
            'x': 114.8536,
            'y': 226.4861,
        }

        def attachment_points(set_no, phase_no, point):
            points = {
                'insulator_attach_point_x': {
                    '1': {
                        '1': 101.4344,
                        '2': 97.0987,
                    }
                },

                'insulator_attach_point_y': {
                    '1': {
                        '1': 207.8282,
                        '2': 216.8395,
                    }
                },
            }

            return points.get(point).get(set_no).get(phase_no)

        self.structure.get_attachment_point.side_effect = attachment_points
        returned = self.lcc.calculate_horiz('1', '2', next_structure)
        self.assertAlmostEqual(returned, -5.0, 2)


        # Segunda prueba
        self.structure.coordinates = {
            'x': 42.3054,
            'y': 187.5299,
        }
        self.structure.sets = ['1']
        self.structure.phases = {
            '1': ['1', '2'],
        }

        next_structure = Mock()
        next_structure.coordinates = {
            'x': 74.4654,
            'y': 186.0302,
        }

        def attachment_points(set_no, phase_no, point):
            points = {
                'insulator_attach_point_x': {
                    '1': {
                        '1': 39.0936,
                        '2': 45.5172,
                    }
                },

                'insulator_attach_point_y': {
                    '1': {
                        '1': 183.6979,
                        '2': 191.3619,
                    }
                },
            }

            return points.get(point).get(set_no).get(phase_no)

        self.structure.get_attachment_point.side_effect = attachment_points
        returned = self.lcc.calculate_horiz('1', '1', next_structure)
        self.assertAlmostEqual(returned, 5.0, 2)


        # Tercera prueba
        self.structure.coordinates = {
            'x': 177.5917,
            'y': 204.6696,
        }
        self.structure.sets = ['1']
        self.structure.phases = {
            '1': ['1', '2'],
        }

        next_structure = Mock()
        next_structure.coordinates = {
            'x': 192.3853,
            'y': 208.3118,
        }

        def attachment_points(set_no, phase_no, point):
            points = {
                'insulator_attach_point_x': {
                    '1': {
                        '1': 184.5651,
                        '2': 168.8783,
                    }
                },

                'insulator_attach_point_y': {
                    '1': {
                        '1': 199.9928,
                        '2': 210.4988,
                    }
                },
            }

            return points.get(point).get(set_no).get(phase_no)

        self.structure.get_attachment_point.side_effect = attachment_points
        returned = self.lcc.calculate_horiz('1', '2', next_structure)
        self.assertAlmostEqual(returned, -10.4873, 2)

        returned = self.lcc.calculate_horiz('1', '1', next_structure)
        self.assertAlmostEqual(returned, 8.3926, 2)


if __name__ == '__main__':
    unittest.main()
