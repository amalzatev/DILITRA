import os
import xml.etree.ElementTree as ET

class PLS_report:
    '''
    Clase para los objetos reportes XML del PLS-CADD.

    arg:
        -filepath (str): Ruta del archivo XML.
    '''
    def __init__(self, filepath):
        self.filepath = filepath
        self.root = self.get_root()

    def get_root(self):
        '''
        Lee un archivo XML y devuelve el elemento root.

        return:
            (xml.etree.ElementTree.Element): Elemento root del XML.
        '''
        
        return ET.parse(self.filepath).getroot()
    

    def get_table(self, lookup_table):
        '''
        Busca y retorna una determinada tabla en el reporte de PLS-CADD segun su atributo tagname.

        arg:
            -lookup_table (str): Nombre de la tabla buscada.

        return:
            -(xml.etree.ElementTree.Element): Tabla buscada.
        '''

        lookup_path = './table[@tagname="' + lookup_table + '"]'
        return self.root.find(lookup_path)


summary_filepath = os.path.join('PLS', 'SM_1x220kV_LasDamas_Portezuelos.xml')
stringingChart_filepath = os.path.join('PLS', 'SC_LT_1x220kV_LasDamas_Portezuelos.xml')

pls_summary = PLS_report(summary_filepath)
pls_SChart = PLS_report(stringingChart_filepath)
