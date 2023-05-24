'''
Clases de los objetos usados por ATPDraw
'''

import pandas as pd
import numpy as np

import xml.etree.ElementTree as ET
from plscadd_report import pls_summary
from plscadd_report import pls_SChart
import os
from xml.dom import minidom


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

class PLS_conductor:
    '''
    Clase para obtener el cable utilizado en cada uno de los vanos
    '''

    def __init__(self, name):
        '''
        Constructor de la clase.

        args:
            -name (str): Nombre de la estructura en el PLS-CADD.
        '''
        self.name = name

    def get_conductor(self, set_no):
        
        '''
        Devuelve el conductor de acuerdo al set para cada uno de los vanos.

        args:
            -set_no(str): Nombre del set buscado.
           
        return:
            -element[0].text: Nombre del conductor 
        '''        

        lookup_table = 'stringing_chart_summary'

        # Se busca en el reporte stringing_chart el nombre del conductor que corresponde a la estrucutra

        stringing_chart_summary = pls_SChart.get_table(lookup_table)
        lookup_path = './' + lookup_table + '/[span_from_str="' + self.name + '"]/[span_from_set="' + set_no + '"]/cable_file_name'

        # element es una lista que contiene el nombre del conductor para diferentes condiciones de temperatura
        element = stringing_chart_summary.findall(lookup_path)

        return element[0].text

class Resistor:
    '''
    Clase para el objeto resistencia de ATPDraw.

    Atributos:
        resistance (float): La resistencia del elemento.
        x_pos (int): Coordenada en x en el lienzo de ATPDraw.
        y_pos (int): Coordenada en y en el lienzo de ATPDraw.
    '''


    def __init__(self, index, resistance, x_pos, y_pos):
        self.resistance = str(resistance)
        self.x_pos = str(x_pos)
        self.y_pos = str(y_pos)
        self.index = str(index + 1)

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
                                                "Angle": str(270),
                                                'PosX': self.x_pos,
                                                'PosY': self.y_pos,
                                                "Output": "1",
                                                'Icon': "default",
                                                },
                                    )

        ET.SubElement(  comp_content, 'node',
                        attrib={
                                'Name': 'From',
                                'Value': self.index + "RPT",
                                "UserNamed": "true",
                                'Kind': '1',
                                'PosX': '-20',
                                'PosY': '0',
                                "NamePosX": "-4",
                                "NamePosY": "0",
                                },
                    )

        ET.SubElement(  comp_content, 'node',
                        attrib={
                                "Name": "To",
                                "Value": "      ",
                                "UserNamed": "true",
                                "Kind": "1",
                                "PosX": "20",
                                "PosY": "0",
                                "NamePosX": "4",
                                "NamePosY": "0",
                                "Ground": "1",
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
        -define_comductors: Extrae el tipo de conductor y agrega los datos relacionados al conductor a phases.info
        -creat_xml_elment: Genera el objeto ElementTree base para el LCC.
    '''

    def __init__(self, id, length, frequency, grnd_resist, structure, alignment, conductors):
        self.id = id
        self.length = length
        self.frequency = frequency
        self.grnd_resist = grnd_resist
        self.structure = structure
        self.conductors = conductors
        self.num_circuits = self.get_num_circuits()
        self.phases_info = self.create_phases()

        self.define_geometry(alignment)
        self.define_conductors()

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
        Crea una tabla (DataFrame) con las fases del LCC. Solo lista el set y la fase a la que corresponden y su tipo. No corresponde a informacion util para ATPDraw.

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

    def define_conductors(self):

        '''
        Agrega los datos relacionados al conductor a los campos de 'Rout', 'Resis', 'React'  a phases.info.

        return:
            -phase_info (pandas.core.frame.DataFrame): Tabla con los datos correspondientes al LCC, agregando los datos correspondientes al conductor'''

        data_conductors = { "800_kcmil_18-19_acar.wir": { "Rin":0, "Rout": 1.265*2,
                                                    "Resis": 0.0833, "Separ": 0, 
                                                    "Alpha":0, "NB":1},
                            "CC-27-27-472-48F.wir": {"Rin":0, "Rout": 1.165*2, 
                                            "Resis": 0.0643, "Separ": 0,
                                            "Alpha":0, "NB":1}}
                            
        Rin = []
        Rout = []
        Resis = []
        Separ = []
        Alpha = []
        NB =[]

        for row in self.phases_info.itertuples():

            set_i = str(getattr(row, 'set'))
            conductor = self.conductors.get_conductor(set_i)
            
            Rin.append(data_conductors[conductor]["Rin"])
            Rout.append(data_conductors[conductor]["Rout"])
            Resis.append(data_conductors[conductor]["Resis"])
            Separ.append(data_conductors[conductor]["Separ"])
            Alpha.append(data_conductors[conductor]["Alpha"])
            NB.append(data_conductors[conductor]["NB"])

        self.phases_info["Rin"] = Rin
        self.phases_info["Rout"] = Rout
        self.phases_info["Resis"] = Resis
        self.phases_info["Separ"] = Separ
        self.phases_info["Alpha"] = Alpha
        self.phases_info["NB"] = NB

    def create_xml_element(self, index, x_pos, y_pos):

        '''
        Genera el objeto ElementTree base para el LCC.

        Atributos:
            index (float): indice para nombrar los nodos del LCC.
            x_pos (int): Coordenada en x en el lienzo de ATPDraw.
            y_pos (int): Coordenada en y en el lienzo de ATPDraw.
            
        Return:
            (xml.etree.ElementTree.Element): Objeto ElementTree.
        '''

        num_phases = len(self.phases_info.index)
        circuits = 1 # definir como se obtiene este valor
        ground = 1 # definir como se obtiene este valor
        Vano = self.structure.get_ahead_span()

        comp = ET.Element(  "comp",
                            attrib={"Name":"LCC", "Id": str(index+1)})
        
        comp_content = ET.SubElement(   comp,
                                        "comp_content",
                                        attrib={
                                                "PosX": str(x_pos),
                                                "PosY": str(y_pos),
                                                "NumPhases": str(num_phases),
                                                "Icon": "default",
                                                "ScaleIconX": "2",
                                                 "ScaleIconY":"2"
                                                },
                                    )

        circuit_name = {"0": "A", "1": "B"}
        DeltaY = -10
        Kind = 1

        for i in range(circuits):

            ET.SubElement(  comp_content,
                            "node",
                            attrib={
                                "Name": "IN{}-{}".format(3 * i + 1, 3 * (i + 1)),
                                "Value": str(index+1) + circuit_name[str(i)] + str(1),
                                "UserNamed": "true",
                                "NumPhases": "3",
                                "Kind": str(Kind),
                                "PosX": "-20",
                                "PosY": str(DeltaY),
                                "NamePosX": "-4",
                                "NamePosY": "-4",
                            },
                        )
        
            DeltaY += 10
            Kind += 1

        circuit_Ground = {"0": "G1-", "1": "G2-"}
        DeltaY = 10

        for i in range(ground):

            ET.SubElement(  comp_content,
                            "node",
                            attrib={
                                "Name": "IN{}".format(num_phases + i),
                                "Value": str(index+1)+ circuit_Ground[str(i)] + str(1),
                                "UserNamed": "false",
                                "Kind": str(Kind),
                                "PosX": "-20",
                                "PosY": str(DeltaY),
                                "NamePosX": "-4",
                                "NamePosY": "-4",
                                },
                            )

            DeltaY += 10
            Kind += 1

        DeltaY = -10
        Kind = 1

        for i in range(circuits):
            ET.SubElement(  comp_content,
                            "node",
                            attrib={
                                "Name": "OUT{}-{}".format(3 * i + 1, 3 * (i + 1)),
                                "Value": str(index+1)+ circuit_name[str(i)] + str(2),
                                "UserNamed": "true",
                                "NumPhases": "3",
                                "Kind": str(Kind),
                                "PosX": "-20",
                                "PosY": str(DeltaY),
                                "NamePosX": "-4",
                                "NamePosY": "-4",
                            },
                        )
            
            DeltaY += 10
            Kind += 1
            
        DeltaY = 10

        for i in range(ground):
            ET.SubElement(  comp_content,
                            "node",
                            attrib={
                                "Name": "OUT{}".format(num_phases + i),
                                "Value": str(index+1) + circuit_Ground[str(i)] + str(2),
                                "UserNamed": "false",
                                "Kind": str(Kind),
                                "PosX": "-20",
                                "PosY": str(DeltaY),
                                "NamePosX": "-4",
                                "NamePosY": "-4",
                            },
                        )
            
            DeltaY += 10
            Kind += 1

        ET.SubElement(  comp_content,
                        "data",
                        attrib={"Name": "Length", "Value": str(Vano)}
        )

        ET.SubElement(  comp_content,
                        "data",
                        attrib={"Name": "Frequency", "Value": str(self.frequency)})

        ET.SubElement(  comp_content,
                        "data",
                        attrib={"Name": "Grnd resist", "Value": str(self.grnd_resist)})

        Comp_LCC = ET.SubElement(comp,
                                    "LCC",
                                    attrib={
                                    "NumPhases": str(num_phases),
                                    "LineCablePipe": "1",
                                    "ModelType": "1",
                                    },
                                    )
        
        line_header = ET.SubElement(Comp_LCC,
                                    "line_header",
                                    attrib={
                                    "RealMtrx": "false",
                                    "SkinEffect": "true",
                                    "AutoBundle": "true",
                                    "MetricUnit": "true",
                                    },
                                    )

        for index, row in self.phases_info.iterrows():


            ET.SubElement(  line_header,
                            "line",
                            attrib={
                            "PhNo":str(index + 1),
                            "Rin":str(row["Rin"]),
                            "Rout":str(row["Rout"]),
                            "Resis":str(row["Resis"]),
                            "React":str(0.2),
                            "Horiz":str(row["Horiz"]),
                            "Vtow":str(row["Vtower"]),
                            "Vmid":str(row["Vtower"]),
                            "NB":str(row["NB"]),
                            "Separ":str(row["Separ"]),
                            "Alpha":str(row["Alpha"]),
                            },
                        )


        return comp

class Probe:
    """
    
    Esta es una clase para crear los probadores de corriente.

    Atributos:
        -ang = Angulo del elemento en ATP.
        -input = Cual es el nombre que se se colocara al punto de entrada del elemento.
        -output = Cual es el nombre que se se colocara al punto de salida del elemento.
        -x_pos = posicion del elemento en x en ATP.
        -y_pos = posicion del elemento en y en ATP.
    Metodos:
        -creat_xml_elment: Genera el objeto ElementTree base para el probe.

    """
    def __init__(self, x_pos, y_pos):

        self.input = str("R")
        self.output = str("G")
        self.x_pos = str(x_pos)
        self.y_pos = str(y_pos)

    
    def create_xml_element(self):
        
        '''
        Genera el objeto ElementTree base para los probadores.

        Return:
            (xml.etree.ElementTree.Element): Objeto ElementTree.
        '''

        comp = ET.Element("comp", attrib={"Name": "PROBE_I"})

        comp_content = ET.SubElement(   comp,
                                        "comp_content", 
                                        attrib={
                                                "PosX": self.x_pos,
                                                "PosY": self.y_pos,
                                                "Icon": "default"
                                                }
                                    )
        
        ET.SubElement(  comp_content,
                        "node",
                        attrib={
                                "Name": "IN",
                                "Value": str(self.input),
                                "UserNamed": "true",
                                "Kind": "1",
                                "PosX": "-20",
                                "PosY": "0",
                                "NamePosX": "-4",
                                "NamePosY": "0",
                                },
                    )
       
        ET.SubElement(  comp_content,
                        "node",
                        attrib={
                                "Name": "OUT",
                                "Value": str(self.output),
                                "UserNamed": "true",
                                "Kind": "1",
                                "PosX": "20",
                                "PosY": "0",
                                "NamePosX": "4",
                                "NamePosY": "0",
                                }
                    )
    
        ET.SubElement(  comp_content,
                        "node",
                        attrib={
                                "Name": "CURR",
                                "Value": "",
                                "Disabled": "true",
                                "Kind": "1",
                                "PosX": "0",
                                "PosY": "-10",
                                "NamePosX": "0",
                                "NamePosY": "-4",
                                }
                    )  
  
        for i in [1, 50, 0]:

            ET.SubElement(  comp_content,
                            "data",
                            attrib={
                                    "Name": "", 
                                    "Value": str(i)
                                    }
                        )

        probe = ET.SubElement(  comp,
                                "probe",
                                attrib={
                                        "CaptureSteadyState": "false",
                                        "OnScreen": "0",
                                        "ScreenFormat": "0",
                                        "ScreenShow": "0",
                                        "CurrNode": "false",
                                        "FontSize": "0",
                                        "Precision": "0",
                                        "TimeOnScreen": "false",
                                        },
                            )
            
        ET.SubElement(  probe,
                        "monitor",
                        attrib={
                                "Phase": "1"
                                }
                    )
        
        return comp
        
class Conn:
    
    """
    
    Esta es una clase para crear los probadores de corriente.

    Atributos:
        -NumPhases = Angulo del elemento en ATP.
        -x_pos1 = posicion inicial del elemento en x en ATP.
        -y_pos1 = posicion inicial del elemento en y en ATP.
        -x_pos2 = posicion final del elemento en x en ATP.
        -y_pos2 = posicion final del elemento en y en ATP.

    Metodos:
        -creat_xml_elment: Genera el objeto ElementTree base para los conectores.
        
    """

    def __init__(self,NumPhases,x_pos1,y_pos1,x_pos2,y_pos2):

        self.x_pos1 = x_pos1
        self.y_pos1 = y_pos1
        self.x_pos2 = x_pos2
        self.y_pos2 = y_pos2
        self.NumPhases = NumPhases

    def create_xml_element(self):
        '''
        Genera el objeto ElementTree base para los conectores.

        Return:
            (xml.etree.ElementTree.Element): Objeto ElementTree.
        '''

        comp = ET.Element("conn")

        ET.SubElement(  comp,
                        "conn_content",
                        attrib={
                                "NumPhases":str(self.NumPhases),
                                "Pos1X":str(self.x_pos1),
                                "Pos1Y":str(self.y_pos1),
                                "Pos2X":str(self.x_pos2),
                                "Pos2Y":str(self.y_pos2)
                                }
                    )
        return comp