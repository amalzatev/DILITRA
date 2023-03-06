from xml.etree.ElementTree import parse, Element
import pandas as pd

nombre_archivo = 'SM_1x220kV_LasDamas_Portezuelos.xml'
doc_xml = parse(nombre_archivo)
root = doc_xml.getroot()

x=root.findall(".//table/[@plsname='Stringing Chart Summary']/stringing_chart_summary/cable_file_name")

List_cables = []

for element in x:

    if element.text[0:-3] not in List_cables:
        List_cables.append(element.text[0:-3])


New_list = [element.text[0:-3] for element in x]

################################
Nivel1 = root.findall("table")
list_Nivel1 = [children.attrib["plsname"] for children in (Nivel1)] # se extrae el nombre de las tablas que corresponden al primer nivel

dicc ={}
################################
for node in list_Nivel1:
    #print(node)
    Nivel2 = root.findall(".//table" +"/[@plsname='" + node + "']/" + node.lower().replace(" ", "_"))
    list_Nivel2 = [children.tag for children in (Nivel2[0].iter())]
    dicc[node] = list_Nivel2

    #print(list_Nivel2)
    #print("*"*100, "\n")




#######################################################################################################

#######################################################################################################


x=root.findall(".//table/[@plsname='Stringing Chart Summary']/stringing_chart_summary/cable_file_name")

List_cables = []
claves = dicc.keys()

dicc2 = {}

for key in dicc.keys():

    diccaux = {}
    Subelements = dicc[key]

    for element1 in dicc[key]:
        U = root.findall(".//table" +"/[@plsname='" + key + "']/" + key.lower().replace(" ", "_") + "/" + element1)
        #print(".//table" +"/[@plsname='" + key + "']/" + key.lower().replace(" ", "_") + "/" + element1)
        New_list = [element.text for element in U]
        if len(New_list) != 0:
            diccaux[element1] = New_list
            dicc2[key] = diccaux
    
        #locals()[key.replace(" ", "_")] = dicc2

for c in dicc2.keys():

    data = pd.DataFrame(dicc2[c])
    #locals()[key.replace(" ", "_")] = pd.DataFrame(dicc2[c])
    print(data)

#print(cont)
#data.to_excel("Prueba1.xlsx")
#print(locals())