import xml.etree.ElementTree as ET

class PLS_report:
    '''
    Clase para los objetos reportes XML del PLS-CADD.
    '''
    def __init__(self, filepath):
        self.filepath = filepath

    def get_root(self):
        '''
        Lee un archivo XML y devuelve el elemento root.
        '''
        
        return ET.parse(self.filepath).getroot()
    


