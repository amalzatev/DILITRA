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
        
        doc_xml = parse(file)
        self.root = doc_xml.getroot()

        self.Nivel1 = self.root.findall("table")
        self.list_Level1 = [children.attrib["plsname"] for children in (self.Nivel1)] # lista de tablas que existan en el xml separadas por espacio

        for node in self.list_Level1:
            # Este ciclo es para obtener los elementos de cada una de las tablas
            # de tal manera que se cree un diccionario que contenga como llave el nombre de la tabla
            # y como valores los elementos que contengan cada tabla

            Nivel2 = self.root.findall(".//table" +"/[@plsname='" + node + "']/" + node.lower().replace(" ", "_"))
            list_Nivel2 = [children.tag for children in (Nivel2[0].iter())]
            self.Dicc_Tags[node] = list_Nivel2

        for key in self.Dicc_Tags.keys():

            # Se crea el diccionario de diccionarios para la extracción de todos los datos

            Dicc_Tagsaux = {}
            self.List_Table.append(key.replace(" ", "_")) # cambiar espacios por _ 

            for element1 in self.Dicc_Tags[key]:

                U = self.root.findall(".//table" +"/[@plsname='" + key + "']/" + key.lower().replace(" ", "_") + "/" + element1)
                New_list = [element.text for element in U]

                if len(New_list) != 0:
                    Dicc_Tagsaux[element1] = New_list
                    self.Dicc_Final[key.replace(" ", "_")] = Dicc_Tagsaux

    def ExtracData(self, table):

        # Extrae la tabla pasada como parametro en un dataframe

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