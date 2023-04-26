'''
Clases de los objetos usados por ATPDraw
'''

import xml.etree.ElementTree as ET
from plscadd_report import pls_summary


class PLS_structure:
    '''
    Clase para el objeto LCC de ATPDraw.

    Atributos:
        -name (str): Nombre de la estructura en el PLS-CADD.
        -attachments (list): Lista con los puntos de sujeción de la estructura. Cada elemento es un diccionario con la información del punto.
        -coordinates (dict): Diccionario con las coordenadas en x, y, z del centro de la estrcutura en metros.
        -ahead_span (float): Vano adelante de la estructura.
    '''

    def __init__(self, name):
        '''
        Constructor de la clase.

        args:
            -name (str): Nombre de la estructura en el PLS-CADD.
        '''
        self.name = name
        self.coordinates = self.get_structure_coordinates()
        self.ahead_span = self.get_ahead_span()
        self.sets = self.get_structure_sets()
        self.phases = self.get_structure_phases(self.sets)

    def get_structure_sets(self):
        '''
        Identifica el conjunto de sets de la estrucutra.

        return:
            -sets (list): Lista con cada uno de los sets de la estructura.'''

        sets = []

        # La información de los sets de la estrcutura se encuentra de la tabla structure_attachment_coordinates del reporte Summary
        lookup_table = 'structure_attachment_coordinates'
        structure_attachment_table = pls_summary.get_table(lookup_table)
        lookup_path = './' + lookup_table + '/[struct_number="' + self.name + '"]/set_no'

        for element in structure_attachment_table.findall(lookup_path):

            # Agregar solo valores unicos
            if element.text not in sets:
                sets.append(element.text)

        return sets

    def get_structure_phases(self, sets):
        '''
        Identifica las fases que contiene cada uno de los sets de la estructura. Devuelve un diccionario con las fases de cada uno de los sets.
        '''

        phases = {}

        # La información de las fases de la estrcutura se encuentra de la tabla structure_attachment_coordinates del reporte Summary
        lookup_table = 'structure_attachment_coordinates'
        structure_attachment_table = pls_summary.get_table(lookup_table)

        for set_i in sets:

            lookup_path = './' + lookup_table + '/[struct_number="' + self.name + '"]/[set_no="' + set_i + '"]/phase_no'
            filtered_elements = structure_attachment_table.findall(lookup_path)

            phases[set_i] = []

            for element in filtered_elements:

                # Agregar solo valores unicos
                if element.text not in phases[set_i]:
                    phases[set_i].append(element.text)

        return phases

    def get_ahead_span(self):
        '''
        Identifica y guarda el vano adelante de la estructura.
        '''

        # La información del vano adelante se extraera de la tabla structure_coordinates_report del reporte Summary
        lookup_table = 'structure_coordinates_report'

        # Se busca en el reporte summary el vano que corresponde a la estrucutra
        structure_coordinates_table = pls_summary.get_table(lookup_table)
        element = structure_coordinates_table.find('./' + lookup_table + '/[struct_number="' + self.name + '"]')
        ahead_span = float(element.find('ahead_span').text)

        return ahead_span

    def get_attachment_point(self, set_no, phase_no, point):
        '''
        Devuelve la coordenada del punto de sujecion especificado.
        '''

        # La información de los puntos de sujeción se encuentra de la tabla structure_attachment_coordinates del reporte Summary
        lookup_table = 'structure_attachment_coordinates'
        structure_attachment_table = pls_summary.get_table(lookup_table)

        lookup_path = './' + lookup_table
        lookup_path = lookup_path + '/[struct_number="' + self.name + '"]'
        lookup_path = lookup_path + '/[set_no="' + set_no + '"]'
        lookup_path = lookup_path + '/[phase_no="' + phase_no + '"]'
        lookup_path = lookup_path + '/' + point

        attachment_point = structure_attachment_table.find(lookup_path).text

        try:
            attachment_point = float(attachment_point)
        except:
            print('\n' + "El punto ingresado no corresponde a un punto de sujecion. No es un numero.")

        return attachment_point


    def get_structure_coordinates(self):
        '''
        Determina las coordenadas del centro de la estructura segun el reporte de PLS-CADD.

                arg:
            pls_report (xml.etree.ElementTree.Element): Elemento root del reporte summary del PLS-CADD.
        '''

        # La información de coordenadas se encuentra en la tabla structure_coordinates_report del reporte Summary
        lookup_table = 'structure_coordinates_report'

        # Se busca en el reporte summary las coordenadas que corresponden a la estrucutra
        structure_coordinates_table = pls_summary.get_table(lookup_table)
        element = structure_coordinates_table.find('./' + lookup_table + '/[struct_number="' + self.name + '"]')

        # Las coordenadas se guarden en un diccionario
        coordinates = {
            'x': float(element.find('x').text),
            'y': float(element.find('y').text),
            'z': float(element.find('z').text),
        }

        return coordinates


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
