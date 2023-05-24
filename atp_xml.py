import xml.etree.ElementTree as ET
from alignment import Alignment
import atp_objects
import os
from xml.dom import minidom

class xml_file:
    
    '''
    Crea el archivo xml de atp con cada uno de los elementos necesarios para la simulación.

    Atributos:
        -pls_summary (xml.etree.ElementTree.Element): Elemento root del reporte Summary.

    Metodos:
        -funcProjecCreate: Crea la configuración inicial del proyecto.
        -funcCompileXML: Crea el archivo .xml.
        -add_object: agrega un elemento al xml_project.
        -create_structures: Crea una lista con los objetos atp_objects.PLS_estructure.
        -create_lcc: Crea una lista con los objetos atp_objects.LCC.
        -create_Resistor: Crea una lista con los objetos atp_objects.Resistor.
        -create_conn: Crea una lista con los objetos atp_objects.Conn.
        -create_probe: Crea una lista con los objetos atp_objects.Probe.
        -create_atp: Agrega cada uno de los elementos al archivo .xml
    '''

    def __init__(self, pls_summary):

        '''
        Constructor de la clase.

        args:
            -pls_summary (xml.etree.ElementTree.Element): Elemento root del reporte Summary.

        '''
        
        self.pls_summary = pls_summary        
        self.structures = self.create_structures()
        self.alignment = Alignment(self.structures)
        self.num_ground = 1
        self.num_circuits = 1
        self.funcProjecCreate()
        self.create_atp()

    def funcProjecCreate(self):
        '''
        Crea la configuración inicial del proyecto con configuraciones generales del atp.

        Return:
            -xml_project (xml.etree.ElementTree.Element): Elemento root del archivo xml.

        '''
        self.xml_project = ET.Element(  "project",
                                        attrib={
                                                "Application": "ATPDraw",
                                                "Version": "7",
                                                "VersionXML": "1"
                                        })

        ET.SubElement(  self.xml_project,
                        "header",
                        attrib={
                                "Timestep2":"1E-6",
                                "Tmax":"0.001",
                                "XOPT":"0",
                                "COPT":"0",
                                "TopLeftX":"4728",
                                "TopLeftY":"4804",
                        },
                    ),
    
        ET.SubElement(  self.xml_project,
                        "objects",
                        attrib={})

    def funcCompileXML(self, strNameXML, strdir):

        '''
        Compila el elemento xml_project para crear el archivo .xml.

        arg: 
            -strNameXML:carpeta y nombre del archivo .xml
            -strdir(str): Ruta de la carpeta desde donde se ejecuta el main

        Return:
            -doc (.xml): Archivo xml.
        '''

        path = os.path.join(strdir, strNameXML)

        self.strXMLfile = minidom.parseString(ET.tostring(self.xml_project)).toprettyxml(
            indent="   "
        )

        doc = open(path + ".xml", "w")
        doc.write(self.strXMLfile)
        doc.close()

    def add_object(self, new_object):
        '''
        Agrega un elemento al xml_project.

        Return:
            -xml_project (xml.etree.ElementTree.Element): Elemento root del archivo xml con el nuevo elemento dentro de objects.

        '''
        objects_tag = self.xml_project.find('objects')
        objects_tag.append(new_object)

    def create_structures(self):
        '''
        Crea los objetos atp_objects.PLS_estructure.

        Return:
            -structures (list): Lista con los objetos atp_objects.PLS_estructure.
        '''

        structures = []
        lookup_table = 'structure_coordinates_report'
        structure_coordinates_table = self.pls_summary.get_table(lookup_table)
        lookup_path = './' + lookup_table + '/struct_number'

        for element in structure_coordinates_table.findall(lookup_path):
            structures.append(atp_objects.PLS_structure(element.text))

        return structures

    def create_lcc(self):

        '''
        Crea los objetos atp_objects.LCC.

        Return:
            -xml_lcc (list): Lista con los objetos atp_objects.LCC.
        '''
        self.xml_lcc = []
        for structure in self.structures[:-1]:

            lcc= atp_objects.LCC(
                    id = structure.name,
                    length = structure.ahead_span / 1000,
                    frequency = 60.0,
                    grnd_resist = 100.0,
                    structure = structure,
                    alignment = self.alignment,
                    conductors = atp_objects.PLS_conductor(structure.name)
                )
            
            index = self.structures.index(structure)
            x_pos = 200 + (index * 160) % 3200
            y_pos = 100 + 300* (index// 20)
            
            self.xml_lcc.append(lcc.create_xml_element(self.structures.index(structure),x_pos,y_pos))
        
        return self.xml_lcc

    def create_Resistor(self):

        '''
        Crea los objetos atp_objects.Resistor.

        Return:
            -xml_resistor (list): Lista con los objetos atp_objects.Resistor.
        '''

        self.xml_resistor = []

        for structure in self.structures[:-1]:

            index = self.structures.index(structure)

            y = 20 if self.num_ground == 2 else 0
            x_pos = 120 + (index * 160) % 3200
            y_pos = 140 + 300 * (index // 20) + y

            resistor= atp_objects.Resistor(
                    index = index,
                    resistance= 20,
                    x_pos=x_pos,
                    y_pos=y_pos
                )
                    
            self.xml_resistor.append(resistor.create_xml_element())
        
        return self.xml_resistor

    def create_conn(self):
        '''
        Crea los objetos atp_objects.Conn.

        Return:
            -xml_conn (list): Lista con los objetos atp_objects.Conn.
        '''

        self.xml_conn = []
        

        for structure in self.structures[:-1]:

            index = self.structures.index(structure)
            for circuit in range(self.num_circuits):

                x_pos = 80 + (index * 160) % 3200
                y_pos = 80 + 300 * (index // 20) + 20*circuit
                x_pos2 = x_pos +  80
                y_pos2 = y_pos

                conn = atp_objects.Conn(
                        NumPhases=3,
                        x_pos1=x_pos,
                        y_pos1=y_pos,
                        x_pos2=x_pos2,
                        y_pos2=y_pos2,
                )

                self.xml_conn.append(conn.create_xml_element())

        return self.xml_conn

    def create_probe(self):
        '''
        Crea los objetos atp_objects.Probe.

        Return:
            -xml_probe (list): Lista con los objetos atp_objects.Probe.
        '''

        self.xml_probe = []

        for structure in self.structures[:-1]:

            index = self.structures.index(structure)
            
            for ground in range(self.num_ground):

                x_pos = 100 + (index * 160) % 3200
                y_pos = 120 + 300 * (index // 20) + 20*ground

                probe = atp_objects.Probe(
                                        x_pos=x_pos,
                                        y_pos=y_pos
                                        )
                
                self.xml_probe.append(probe.create_xml_element())
                            
                probe = atp_objects.Probe(
                                        x_pos=x_pos+40,
                                        y_pos=y_pos
                                        )

                self.xml_probe.append(probe.create_xml_element())

        return self.xml_probe

    def create_atp(self):
        '''
        Itera sobre acada una de las listas para cada componente y los agrega al xml_project.

        '''
        
        xml_resistor = self.create_Resistor()
        xml_lcc = self.create_lcc()
        xml_conn = self.create_conn()
        xml_probe = self.create_probe()

        c_circuit = 0
        c_ground = 0

        for structure in self.structures[:-1]:

            index = self.structures.index(structure)
            self.add_object(xml_resistor[index])
            self.add_object(xml_lcc[index])

            for circuit in range(self.num_circuits):
                self.add_object(xml_conn[c_circuit])
                c_circuit += 1
            
            for ground in range(self.num_ground):
                for i_probe in range(2):

                    self.add_object(xml_probe[c_ground])
                    c_ground += 1


        self.funcCompileXML("ATP/" + "Version1",os.getcwd())
