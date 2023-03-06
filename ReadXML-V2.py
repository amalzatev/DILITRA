from xml.etree.ElementTree import parse, Element
import pandas as pd

nombre_archivo = 'SM_1x220kV_LasDamas_Portezuelos.xml'
doc_xml = parse(nombre_archivo)
root = doc_xml.getroot()

################################
Nivel1 = root.findall("table")
list_Nivel1 = [children.attrib["plsname"] for children in (Nivel1)] # se extrae el nombre de las tablas que corresponden al primer nivel


################################
# se estraen los nombres de los subelementos para cada nivel y se agregan a un Diccionario

Dicc_Etiquetas ={}
for node in list_Nivel1:
    
    Nivel2 = root.findall(".//table" +"/[@plsname='" + node + "']/" + node.lower().replace(" ", "_"))
    list_Nivel2 = [children.tag for children in (Nivel2[0].iter())]
    Dicc_Etiquetas[node] = list_Nivel2

#######################################################################################################

Dicc_Etiquetas2 = {}

for key in Dicc_Etiquetas.keys():

    Dicc_Etiquetasaux = {}

    for element1 in Dicc_Etiquetas[key]:

        U = root.findall(".//table" +"/[@plsname='" + key + "']/" + key.lower().replace(" ", "_") + "/" + element1)
        New_list = [element.text for element in U]

        if len(New_list) != 0:
            Dicc_Etiquetasaux[element1] = New_list
            Dicc_Etiquetas2[key] = Dicc_Etiquetasaux

for c in Dicc_Etiquetas2.keys():
    print(c)
    data = pd.DataFrame(Dicc_Etiquetas2[c])
    #locals()[key.replace(" ", "_")] = pd.DataFrame(Dicc_Etiquetas2[c])
    #print(data)

print(Dicc_Etiquetas)
#data.to_excel("Prueba1.xlsx")
#print(locals())