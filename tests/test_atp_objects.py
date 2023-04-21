import unittest


class TestMathUtils(unittest.TestCase):
    
    def test_Resistor_create_xml_element(self):
        expected = '''
        <comp Name="RESISTOR">
        <comp_content PosX="4710" PosY="4940" Icon="default">
            <node Name="From" Value="" Kind="1" PosX="-20" PosY="0" NamePosX="-4" NamePosY="0"/>
            <node Name="To" Value="" Kind="1" PosX="20" PosY="0" NamePosX="4" NamePosY="0"/>
            <data Name="R" Value="1000"/>
        </comp_content>
        </comp>
        '''

        
