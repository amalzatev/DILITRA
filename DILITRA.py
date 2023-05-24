'''
Script principal
'''

import xml.etree.ElementTree as ET
from plscadd_report import pls_summary
from atp_objects import PLS_structure
from atp_objects import PLS_conductor
from alignment import Alignment
from atp_objects import LCC
from atp_xml import xml_file

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
        structures.append(PLS_structure(element.text))

    return structures

def create_lcc(structures, alignment):

    lcc = []
    for structure in structures[:-1]:

        lcc.append(
            LCC(
                id = structure.name,
                length = structure.ahead_span / 1000,
                frequency = 60.0,
                grnd_resist = 100.0,
                structure = structure,
                alignment = alignment,
                conductors = PLS_conductor(structure.name)
            )
        )

    return lcc

def main():

    structures = create_structures(pls_summary)
    alignment = Alignment(structures)
    lcc_list = create_lcc(structures, alignment)
    atp = xml_file(pls_summary=pls_summary,alignment=alignment)
    atp.create_atp


    

if __name__ == '__main__':
    main()
