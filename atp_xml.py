import xml.etree.ElementTree as ET
from plscadd_report import pls_summary
from alignment import Alignment
import atp_objects
import os

def create_structures(pls_summary):
    '''
    Crea los objetos atp_objects.PLS_estructure.

    arg:
        -pls_summary (xml.etree.ElementTree.Element): Elemento root del reporte Summary.

    Return:
        -structures (list): Lista con los objetos atp_objects.PLS_estructure.
    '''

    structures = []
    lookup_table = 'structure_coordinates_report'
    structure_coordinates_table = pls_summary.get_table(lookup_table)
    lookup_path = './' + lookup_table + '/struct_number'

    for element in structure_coordinates_table.findall(lookup_path):
        structures.append(atp_objects.PLS_structure(element.text))

    return structures

def create_lcc(structures, alignment):

    xml_lcc = []
    for structure in structures[:-1]:

        lcc= atp_objects.LCC(
                id = structure.name,
                length = structure.ahead_span / 1000,
                frequency = 60.0,
                grnd_resist = 100.0,
                structure = structure,
                alignment = alignment,
                conductors = atp_objects.PLS_conductor(structure.name)
            )
        
        index = structures.index(structure)
        x_pos = 200 + (index * 160) % 3200
        y_pos = 100 + 300* (index// 20)
        
        xml_lcc.append(lcc.create_xml_element(structures.index(structure),x_pos,y_pos))
    
    return xml_lcc

def create_Resistor(structures):

    xml_resistor = []

    for structure in structures[:-1]:

        index = structures.index(structure)

        num_ground = 1 # definir una función que determine el numero de cables de guardia
        

        y = 20 if num_ground == 2 else 0
        x_pos = 120 + (index * 160) % 3200
        y_pos = 140 + 300 * (index // 20) + y

        resistor= atp_objects.Resistor(
                index = index,
                resistance= 20,
                x_pos=x_pos,
                y_pos=y_pos
            )
                
        xml_resistor.append(resistor.create_xml_element())
    
    return xml_resistor

def create_conn(structures):

    xml_conn = []
    num_circuits = 1

    for structure in structures[:-1]:

        index = structures.index(structure)
        y = 0
        for circuit in range(num_circuits):

            x_pos = 80 + (index * 160) % 3200
            y_pos = 80 + 300 * (index // 20) + y
            x_pos2 = x_pos +  80
            y_pos2 = y_pos
            y = 20

            conn = atp_objects.Conn(
                    NumPhases=3,
                    x_pos1=x_pos,
                    y_pos1=y_pos,
                    x_pos2=x_pos2,
                    y_pos2=y_pos2,
            )
            xml_conn.append(conn.create_xml_element())
    return xml_conn

def create_probe(structures):

    xml_probe = []
    num_ground = 1

    for structure in structures[:-1]:

        index = structures.index(structure)
        y = 0

        for ground in range(num_ground):

            x_pos = 100 + (index * 160) % 3200
            y_pos = 120 + 300 * (index // 20) + y
            y = 20

            probe = atp_objects.Probe(
                                    x_pos=x_pos,
                                    y_pos=y_pos
                                    )
            
            xml_probe.append(probe.create_xml_element())
                        
            probe = atp_objects.Probe(
                                    x_pos=x_pos+40,
                                    y_pos=y_pos
                                      )

            xml_probe.append(probe.create_xml_element())

    return xml_probe


atp = atp_objects.xml_file()
atp.funcProjecCreate()

structures = create_structures(pls_summary)
alignment = Alignment(structures)

xml_lcc = create_lcc(structures, alignment)
xml_resistor = create_Resistor(structures)
xml_conn = create_conn(structures)
xml_probe = create_probe(structures)

c_circuit = 0
c_ground = 0
num_circuits = 1
num_ground = 1

for structure in structures[:-1]:

    index = structures.index(structure)
    atp.add_object(xml_resistor[index])
    atp.add_object(xml_lcc[index])

    for circuit in range(num_circuits):
        atp.add_object(xml_conn[c_circuit])
        c_circuit += 1
    
    for ground in range(num_ground):
        for i_probe in range(2):

            atp.add_object(xml_probe[c_ground])
            c_ground += 1


atp.funcCompileXML("ATP/" + "Version1",os.getcwd())
