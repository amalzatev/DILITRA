'''
Clases de los objetos usados por ATPDraw
'''

import xml.etree.ElementTree as ET


class PLS_structure:
    '''
    Clase para el objeto LCC de ATPDraw.

    Atributos:
        -name (str): Nombre de la estructura en el PLS-CADD.
        -attachments (list): Lista con los puntos de sujeción de la estructura. Cada elemento es un diccionario con la información del punto.
    '''

    def __init__(self, name, pls_report):
        '''
        Constructor de la clase.

        args:
            -name (str): Nombre de la estructura en el PLS-CADD.
            -pls_report (xml.etree.ElementTree.Element): Elemento root del reporte summary del PLS-CADD.
        '''
        self.name = name
        self.get_attachment_points(pls_report)
        self.get_structure_coordinates(pls_report)

    def get_attachment_points(self, pls_report):
        '''
        Crea una lista con los puntos de sujeción de la estructura.
        Cada elemento de la lista es un punto representado por un diccionario con la información del set, fase y las coordenadas de sujeción del conductor y el aislador.

        arg:
            pls_report (xml.etree.ElementTree.Element): Elemento root del reporte summary del PLS-CADD.
        '''

        # Inicialización de la lista que contendrá los puntos de sujeción
        self.attachments = []

        # Diccionario auxiliar para almacenar punto por punto que luego será agregado a attachments
        attachment_point = {}

        # La información de los puntos de sujeción se encuentra en la tabla structure_attachment_coordinates del reporte Summary
        lookup_table = 'structure_attachment_coordinates'

        # Se itera sobre el reporte summary buscando los puntos que corresponden a la estrucutra self.name
        for element in pls_report.findall('./table[@tagname="' + lookup_table + '"]/' + lookup_table + '/[struct_number="' + self.name + '"]'):

            attachment_point['set_no'] = element.find('set_no').text
            attachment_point['phase_no'] = element.find('phase_no').text

            attachment_point['insulator_attach_point'] = {
                'x': element.find('insulator_attach_point_x').text,
                'y': element.find('insulator_attach_point_y').text,
                'z': element.find('insulator_attach_point_z').text,
            }

            attachment_point['wire_attach_point'] = {
                'x': element.find('wire_attach_point_x').text,
                'y': element.find('wire_attach_point_y').text,
                'z': element.find('wire_attach_point_z').text,
            }

            attachment_point['section_number'] = element.find('section_number').text

            # Luego de crear el diccionario para un punto, este se añade a la lista attachments
            self.attachments.append(attachment_point.copy())

        return self.attachments

    def get_structure_coordinates(self, pls_report):
        '''
        Determina las coordenadas del centro de la estructura segun el reporte de PLS-CADD.

                arg:
            pls_report (xml.etree.ElementTree.Element): Elemento root del reporte summary del PLS-CADD.
        '''

        # La información de coordenadas se encuentra en la tabla structure_coordinates_report del reporte Summary
        lookup_table = 'structure_coordinates_report'

        # Se busca en el reporte summary las coordenadas que corresponden a la estrucutra self.name
        element = pls_report.find('./table[@tagname="' + lookup_table + '"]/' + lookup_table + '/[struct_number="' + self.name + '"]')

        # Las coordenadas se guarden en un diccionario
        self.coordinates = {
            'x': element.find('x').text,
            'y': element.find('y').text,
            'z': element.find('z').text,
        }

        return self.coordinates


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
