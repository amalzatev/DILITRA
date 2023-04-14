from xml.etree.ElementTree import parse, Element
import pandas as pd
import os


class ReadXML:
    """
    Esta Función se encarga de extraer los datos en un diccionario de diccionarios
    en donde por cada tabla hay un diccionario que tiene como valores otro diccionario
    con los atributos correspondientes.
    """

    def __init__(self, file):

        self.file = file
        self.list_Level1 = list()
        self.Dicc_Tags = dict()
        self.Dicc_Final = dict()
        self.List_Table = list()
        self.readData(file)

    def readData(self, file):
        '''
        Crea un diccionario con las tablas del reporte, donde cada uno de sus elementos es otro diccionario con sus campos y valores.

        Args:
            file (str): La ruta del archivo XML del informe PLS-CADD.
        '''
        
        # Leer el archivo XML y obtener el elemento root
        doc_xml = parse(file)
        self.root = doc_xml.getroot()

        # Lista con los nombres de todas las tablas del reporte
        self.Nivel1 = self.root.findall("table")
        self.list_Level1 = [children.attrib["plsname"] for children in (self.Nivel1)]

        for node in self.list_Level1:

            # Este ciclo obtiene los campos de cada una de las tablas.
            # El resultado es un diccionario con el nombre de la tabla como llave y en sus valores los campos que componen cada tabla.
            # Itera sobre los nombres de las tablas del reporte.

            # Lista con el nombre de los que conforman cada una de las tablas
            Nivel2 = self.root.findall(".//table" +"/[@plsname='" + node + "']/" + node.lower().replace(" ", "_"))
            list_Nivel2 = [children.tag for children in (Nivel2[0].iter())] # El Nivel2[0] significa que usa solo la primera fila de la tabla (rownum='0')
            
            # Diccionario con el nombre de las tablas y sus campos respectivos
            self.Dicc_Tags[node] = list_Nivel2

        for key in self.Dicc_Tags.keys():

            # Se crea el diccionario de diccionarios con todos los datos del reporte
            # Itera sobre los nombres de las tablas del reporte.

            Dicc_Tagsaux = {}

            # Añadir de una en una los nombres de las tablas a la lista de tablas
            self.List_Table.append(key.replace(" ", "_")) # cambiar espacios por _ 

            for element1 in self.Dicc_Tags[key]:

                # Itera sobre los nombres de los campos de la tabla

                # Busca los elementos de cada uno de los campos de la tabla
                U = self.root.findall(".//table" +"/[@plsname='" + key + "']/" + key.lower().replace(" ", "_") + "/" + element1)

                # Se obtienen los valores de cada uno de los campos
                New_list = [element.text for element in U]

                # Se discriminan las listas vacias porque la primera siempre lo sera debido al Element.iter() de antes que devuelve el propio nombre del elemento al que itera
                if len(New_list) != 0:
                    
                    # Se crea el diccionario cuya llave es el campo de la tabla y los valores son los valores de cada fila en la tabla
                    Dicc_Tagsaux[element1] = New_list

                    # Se crea el diccionario resultado modificando las llaves para eliminar los espacios
                    self.Dicc_Final[key.replace(" ", "_")] = Dicc_Tagsaux

    def ExtracData(self, table):

        '''
        Convierte en DaraFrame un diccionario que contiene la informacion de una de las tablas del reporte PLS-CADD.

        Args:
            table (str): Nombre de la tabla a extraer que sera una de las llaves de Dicc_Final.

        Returns:
            pd.DataFrame: DataFrame de la tabla buscada.
        '''

        return  pd.DataFrame(self.Dicc_Final[table])
        


#########################################################################################################
##                                     Exportar los datos a tabla de Excel                             ##
#########################################################################################################


# data = ReadXML('PLC/SM_1x220kV_LasDamas_Portezuelos.xml')
# print(data.list_Level1)
# Summary = data.Dicc_Final
# Tables = data.List_Table


# writer = pd.ExcelWriter('Prueba.xlsx')

# Structure_List_Report = data.Structure_List_Report
# Cable_Material_List_Report = data.Cable_Material_List_Report

# for table in Tables:

#     Data_Frame = data.ExtracData(table)
#     Data_Frame.to_excel(writer, table, index=False)
# Structure_List_Report.to_excel(writer, "Structure_List_Report", index=False)
# Cable_Material_List_Report.to_excel(writer, "Cable_Material_List_Report", index=False)
# writer.save()
# writer.close()