'''
Clases de los objetos usados por ATPDraw
'''

import pandas as pd
import numpy as np

import xml.etree.ElementTree as ET
from plscadd_report import pls_summary


class PLS_structure:
    '''
    Clase para el objeto LCC de ATPDraw.

    Atributos:
        -name (str): Nombre de la estructura en el PLS-CADD.
        -coordinates (dict): Diccionario con las coordenadas en x, y, z del centro de la estrcutura en metros.
        -ahead_span (float): Vano adelante de la estructura.
        -sets (list): Lista con cada uno de los sets de la estructura.
        -phases (dict): Diccionario cuyas llaves son los sets de la estructura y sus valores son una lista con las fases de cada uno de los sets.

    Metodos:
        get_structure_sets: Identifica el conjunto de sets de la estrucutra.
        get_structure_phases: Identifica las fases que contiene cada uno de los sets de la estructura. Devuelve un diccionario con las fases de cada uno de los sets.
        get_ahead_span: Identifica y guarda el vano adelante de la estructura.
        get_attachment_point: Devuelve la coordenada del punto de sujecion especificado.
        get_structure_coordinates: Determina las coordenadas del centro de la estructura.
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

        arg:
            -sets (list): Lista con cada uno de los sets de la estructura.

        return:
            -phases(dict): Diccionario cuyas llaves son los sets de la estructura y sus valores son una lista con las fases de cada uno de los sets.
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

        return:
            -ahead_span(float): Longitud del vano adelante de la estructura en metros.
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

        args:
            -set_no(str): Nombre del set buscado.
            -phase_no(str): Nombre de la fase buscada.
            -point(str): Nombre del punto buscado. Debe corresponder con los campos que trae el reporte XML de PLS-CADD.

        return:
            -attachment_point(float): Coordenada del punto buscado.
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
            print('\n' + "El campo " + point + " no corresponde a un punto de sujeción.")

        return attachment_point

    def get_structure_coordinates(self):
        '''
        Determina las coordenadas del centro de la estructura.

        return:
            -coordinates(dict): Diccionario con las coordenadas x, y, z.
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


class LCC:
    '''
    Clase para el objetco LCC de ATPDraw.

    Atributos:
        -id(str): Nombre del LCC.
        -length(float): Longitud del vano en km.
        -frequency(float): Frecuencia industrial del sistema en Hz.
        -grnd_resist(float): Resistividad del terreno en Ohm-m.
        -structure(atp_objects.PLS_structure): Estructura de la cual nace el vano.
        -phase_info (pandas.core.frame.DataFrame): Tabla con el listado de las fases del LCC.

    Metodos:
        -get_num_circuits: Determina el numero de circuitos del LCC según los sets de la estructura del PLS-CADD.
        -get_num_phases: Determina el numero de fases del LCC según los sets de la estructura del PLS-CADD.
        -create_phases: Crea una tabla (DataFrame) con las fases del LCC. Solo lista el set y lafase a la que corresponden y su tipo. No corresponde a informacion util para ATPDraw.
        -define_geometry: Calcula la posicion geometrica de cada fase con respecto al cntro de la estrucutra. Agrega los campos de 'Horiz' y 'Vtower' a phases.info.
    '''

    def __init__(self, id, length, frequency, grnd_resist, structure, alignment):
        self.id = id
        self.length = length
        self.frequency = frequency
        self.grnd_resist = grnd_resist
        self.structure = structure
        self.num_circuits = self.get_num_circuits()
        self.phases_info = self.create_phases()

        self.define_geometry(alignment)


    def get_num_circuits(self):
        '''
        Determina el numero de circuitos del LCC según los sets de la estructura del PLS-CADD.

        return:
            -num_circuits(int): Numero de circuitos.
        '''

        num_circuits = 0
        for set_i in self.structure.sets:
            if set_i[0] != '1':
                num_circuits += 1

        return num_circuits

    def get_num_phases(self):
        '''
        Determina el numero de fases del LCC según los sets de la estructura del PLS-CADD.
        '''
        return len(self.structure.sets)

    def create_phases(self):
        '''
        Crea una tabla (DataFrame) con las fases del LCC. Solo lista el set y lafase a la que corresponden y su tipo. No corresponde a informacion util para ATPDraw.

        return:
            -phase_info (pandas.core.frame.DataFrame): Tabla con el listado de las fases del LCC.
        '''

        sets = []
        phases = []
        for set_i, set_phases in self.structure.phases.items():
            for phase_i in set_phases:
                sets.append(set_i)
                phases.append(phase_i)

        phase_info = pd.DataFrame({'set': sets, 'phase': phases})
        set_type = {'1': 'ground', '2': 'phase'}
        phase_info['type'] = phase_info['set'].map(set_type)
        phase_info.sort_values('type', ascending=False, inplace=True)
        phase_info.reset_index(drop=True, inplace=True)
        return phase_info

    def define_geometry(self, alignment):
        '''
        Calcula la posicion geometrica de cada fase con respecto al cntro de la estrucutra. Agrega los campos de 'Horiz' y 'Vtower' a phases.info.

        args:
            -alignment (alignment.Alignment): Instancia del alineamiento de la linea.
            '''

        horiz = []
        v_tower = []
        for row in self.phases_info.itertuples():
            set_i = str(getattr(row, 'set'))
            phase_i = str(getattr(row, 'phase'))

            point_x = self.structure.get_attachment_point(set_i, phase_i, 'insulator_attach_point_x')
            point_y = self.structure.get_attachment_point(set_i, phase_i, 'insulator_attach_point_y')
            point = np.array([point_x, point_y])

            point = alignment.align_point(point, self.structure.name)

            mult = 1
            if point[0] < 0:
                mult = -1
            horiz.append(mult * np.sqrt(point[0]**2 + point[1]**2))


            point_z = self.structure.get_attachment_point(set_i, phase_i, 'insulator_attach_point_z')

            v_tower.append(point_z - self.structure.coordinates.get('z'))

        self.phases_info['Horiz'] = horiz
        self.phases_info['Vtower'] = v_tower
