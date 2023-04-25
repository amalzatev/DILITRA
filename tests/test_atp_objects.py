import unittest
import xml.etree.ElementTree as ET

import os
import sys
sys.path.append(os.getcwd())

from atp_objects import Resistor


class Test_ATPObjects(unittest.TestCase):

    def setUp(self):
        self.resistor = Resistor(
                            resistance = 1000,
                            x_pos = 4710,
                            y_pos = 4940,
                            )


    def test_Resistor_int_resistance(self):
        '''
        Testear que el valor de la resistencia se asignó adecuadamente.
        '''

        self.xml_element = self.resistor.create_xml_element()
        data_element = self.xml_element.find('./comp_content/data')
        self.assertEqual(data_element.get('Value'), '1000')

    def test_Resistor_xml_element_has_correct_estructure(self):
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


if __name__ == '__main__':
    unittest.main()
