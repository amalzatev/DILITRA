'''
Script principal
'''


from plscadd_report import pls_summary
from atp_objects import PLS_structure

def create_structures(summary_root):
    '''
    Crea los objetos atp_objects.PLS_estructure.

    arg:
        -summary_root (xml.etree.ElementTree.Element): Elemento root del reporte Summary.

    Return:
        -structures (list): Lista con los objetos atp_objects.PLS_estructure.
    '''

    structures = []
    lookup_table = 'structure_coordinates_report'
    structure_coordinates_table = summary_root.get_table(lookup_table)
    lookup_path = './' + lookup_table + '/struct_number'
    for element in structure_coordinates_table.findall(lookup_path):
        structures.append(PLS_structure(element.text))

    return structures

def main():

    estructures = create_structures(pls_summary.root)

    for estructure in estructures:
        print(estructure.name)



    # Crear las estructuras
    # estructures = create_estructures(pls_data)

if __name__ == '__main__':
    main()
