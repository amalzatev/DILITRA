'''
Clases de los objetos usados por ATPDraw
'''

import xml.etree.ElementTree as ET

class Resistor:
    '''
    Clase para el objeto resistencia de ATPDraw.

    Atributos:
        resistance (float): La resistencia del elemento.
        x_pos (int): Coordenada en x en el lienzo de ATPDraw.
        y_pos (int): Coordenada en y en el lienzo de ATPDraw.
    '''
    
    
    def __init__(self, resistance, x_pos, y_pos):
        self.resistance = str(resistance)
        self.x_pos = str(x_pos)
        self.y_pos = str(y_pos)
    
    def create_xml_element(self):
        '''
        Genera el objeto ElementTree base de la resistencia.

        Return:
            (xml.etree.ElementTree.Element): Objeto ElementTree.
        '''

        comp = ET.Element(  'comp',
                            attrib={'Name': 'RESISTOR'},
                        )

        comp_content = ET.SubElement(   comp,
                                        'comp_content',
                                        attrib={
                                                'PosX': self.x_pos,
                                                'PosY': self.y_pos,
                                                'Icon': "default",
                                                },
                                    )

        ET.SubElement(  comp_content, 'node',
                        attrib={
                                'Name': 'From',
                                'Value': '',
                                'Kind': '1',
                                'PosX': '-20',
                                'PosY': '0',
                                },
                    )

        ET.SubElement(  comp_content, 'node',
                        attrib={
                                'Name': 'To',
                                'Value': '',
                                'Kind': '1',
                                'PosX': '20',
                                'PosY': '0',
                                },
                    )

        ET.SubElement(  comp_content, 'data',
                        attrib={
                                'Name': 'R',
                                'Value': self.resistance,
                                'Kind': '1',
                                },
                    )

        return comp
