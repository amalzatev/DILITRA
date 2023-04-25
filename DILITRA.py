'''
Script principal
'''


from plscadd_report import PLS_report
from atp_objects import PLS_estructure

def create_estructures(root):
    '''
    Crea los objetos atp_objects.PLS_estructure.

    arg:
        -root (xml.etree.ElementTree.Element): Elemento root del reporte Summary.

    Return:
        -estructures (list): Lista con los objetos atp_objects.PLS_estructure.
    '''


    estructures = []
    structure_coordinates_report_path = "./table[@tagname='structure_coordinates_report']/*"
    for estructure in root.findall(structure_coordinates_report_path):
        name = estructure.find('structure_name').text
        estructure_object = PLS_estructure(name)
        estructure_object.get_attachment_coordinates(root)
        # estructures.append()


    return estructures




def main():

    # Se lee el reporte Summary del PLS-CADD
    summary_filepath = 'PLS\SM_1x220kV_LasDamas_Portezuelos.xml'
    summary_root = PLS_report(summary_filepath).get_root()

    estructures = create_estructures(summary_root)

    for estructure in estructures:
        print(estructure.name)



    # Crear las estructuras
    # estructures = create_estructures(pls_data)

if __name__ == '__main__':
    main()
