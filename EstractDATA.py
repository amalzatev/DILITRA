import pandas as pd
from READXML.ReadFileXML import ReadXML
import numpy as np
import XMLATP
import XLSX2ATP
import pandas as pd
import xml.etree.ElementTree as ET
import os

# Se estraen los datos con la funcion ReadFileXML de tal manera que se pueden tener acceso a cualquiera de las
# tablas que se obtienen desde el PLSCad

data = ReadXML('PLC/SM_1x220kV_LasDamas_Portezuelos.xml')
Summary = data.Dicc_Final
Tables = data.List_Table
St_Coordinates = data.ExtracData('Structure_Coordinates_Report')
Stringing_Data= data.ExtracData("Section_Stringing_Data")


#############################################################
##    Datos Para Resistencias de Puesta a tierra           ##
#############################################################

data_RPT = {"Nombre":list(St_Coordinates["struct_number"]),"RPT": []}


for Nombre in range(len(list(St_Coordinates["struct_number"]))):
    data_RPT["RPT"].append(20)


#############################################################
##                    Datos Para LCC                       ##
#############################################################

General_Data = {"Nombre": list(St_Coordinates["struct_number"]), "Longitud": list(St_Coordinates["ahead_span"]), "Resistividad":100,
        "Separacion conductores": 0, "Angulo" :0, "NB": 0,
        "Circuitos": 1, "Ground": 1, "Frecuencia": 50}  # los demas datos son especificados por el usuario

# Los datos del conductor son especificados por el usuario
Conductores = {"C1": {"Diametro": 1.265*2, "Resistencia DC": 0.0833, "Reactancia":0.5169},
               "CG1": {"Diametro": 1.165*2, "Resistencia DC": 0.0643, "Reactancia":0.3369}}

# Se agregan los set
Set = {"C1": "2", "CG1": "1"}

# Se crea el diccionario con las llaves segun el numero de circuitos y Guardas
Cable_Data = {"Nombre":[]}

for i in range(General_Data["Circuitos"]):
    Cable_Data["C" + str(i+1)] = []

for i in range(General_Data["Ground"]):
    Cable_Data["CG" + str(i+1)] = []



# se crea un dataframe con los datos de los cables segun corresponda el set
for clave in Set:

    aux = [] #lista auxiliar para separar el conductor de fase y los cables de guarda

    for i in range(Stringing_Data.shape[0]):

        if Stringing_Data["struct_number"].iloc[i] not in aux and Stringing_Data["set_number"].iloc[i] == Set[clave]:
            
            aux.append(Stringing_Data["struct_number"].iloc[i])
            Cable_Data[clave].append(Conductores[clave])
    Cable_Data["Nombre"] = aux

DF_Cond_data = pd.DataFrame(Cable_Data)


#--------------------------------> Extraer Datos de la geometria desde los archivos del PLC <----------------------------------#

St_Att_Coordinates = data.ExtracData('Structure_Attachment_Coordinates')

# Se crea el diccionario con las llaves segun el numero de circuitos y Guardas
Geometrias = {"Nombre":[]}

for i in range(General_Data["Circuitos"]):
    for j in range(3):
        Geometrias["C" + str(i+1) + "-" + str(j+1)] = []

for i in range(General_Data["Ground"]):
    Geometrias["CG" + str(i+1) + "-1"] = []


# Se crea el Dataframe con las geometrias de las torres
for i in range(len(St_Coordinates)):

    Structure = St_Coordinates.iloc[i]["struct_number"]
    Data_Str = St_Att_Coordinates[St_Att_Coordinates["struct_number"] == Structure]

    for Fila in range(len(Data_Str)):
        
        aux = {}
        
        Z_ins = Data_Str.iloc[Fila]["insulator_attach_point_z"]
        Z_wire = Data_Str.iloc[Fila]["wire_attach_point_z"]
        x1_x2 = float(St_Coordinates.iloc[i]["x"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_x"])
        y1_y2 = float(St_Coordinates.iloc[i]["y"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_y"])
        z1_z2 = float(St_Coordinates.iloc[i]["z"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_z"])

        if Z_ins == Z_wire:
            
            aux["Horiz"] = np.round(np.sqrt(x1_x2**2 + y1_y2**2),2)
            aux["Vtow"] = np.round(np.abs(z1_z2),2)
            aux["Vmid"] = np.round(np.abs(z1_z2),2)

            for clave in Set:

                if Set[clave] == Data_Str.iloc[Fila]["set_no"]:

                    Geometrias[clave + "-" +  Data_Str.iloc[Fila]["phase_no"]].append(aux)


        else:

            X = np.round(np.sqrt(x1_x2**2 + y1_y2**2), 2)
            X1 = -X if (x1_x2 < 0) else X

            aux["Horiz"] = np.round(X1,2)
            aux["Vtow"] = np.round(np.abs(z1_z2),2)
            aux["Vmid"] = np.round(np.abs(z1_z2),2)

            for clave in Set:

                if Set[clave] == Data_Str.iloc[Fila]["set_no"]:

                    Geometrias[clave + "-" +  Data_Str.iloc[Fila]["phase_no"]].append(aux)


    Geometrias["Nombre"].append(Structure)

DF_Geometrias = pd.DataFrame(Geometrias)


########################################################################
##                  Crear XML despues de obtener los datos            ##
########################################################################

atp = XMLATP.XMLFILE()
atp.funcProjecCreate()
ET.SubElement(atp.xmlProject,
            "header",
            attrib={
                "Timestep2":"1E-6",
                "Tmax":"0.001",
                "XOPT":"0",
                "COPT":"0",
                "TopLeftX":"4728",
                "TopLeftY":"4804",
            },
        ),

Level_object = ET.Element("objects",{})

#############################################################
#             Creacion de elementos multiples              ##
#############################################################


for Torre in range(len(data_RPT["Nombre"])):

    # se agregan las resistencias para cada una de las torres, en este punto se pueden tambien cambiar las RPT
    y = 10 if General_Data["Ground"] == 2 else 0
    posx = 140 + (100 + Torre * 120) % 2400
    posy = 170 + 300 * (1 + Torre // 20) + y
    dic1 = XLSX2ATP.Resistor(Torre,data_RPT["RPT"][Torre], posx, posy)
    Level_object.append(dic1.ET)


    # Se agregan los LCC solo para un caso ejemplo
    geometry = DF_Geometrias.iloc[Torre]# en este punto se itera sobre la geometria de todas las torres ############# Se debe cambiar
    Conductor_Data = DF_Cond_data.iloc[Torre]
    posx = 200 + (100 + Torre * 120) % 2400
    posy = 100 + 300* (1 + Torre// 20)
    LCC1 = XLSX2ATP.Tower(Torre,geometry,General_Data,Conductor_Data,posx, posy)
    Level_object.append(LCC1.ET)


    # se agregan los connectores trifasicos
    y = 0
    for i in range(General_Data["Circuitos"]):

        posx1 = 220 + (100 + Torre * 120) % 2400
        posy1 = 90 + 300 * (1 + Torre // 20) + y
        posx2 = posx1 +  80
        posy2 = posy1
        y = 10
        CONN = XLSX2ATP.Conn(3,posx1,posy1,posx2,posy2)
        Level_object.append(CONN.ET)


    # se agregan los probadores que van dentro del cable de guardia
    y = 0
    for i in range(General_Data["Ground"]):

        # numero de cables de guardia para este caso se asumen dos
        posx1 = 220 + (100 + Torre * 120) % 2400
        posy1 = 110 + 300 * (1 + Torre // 20) + y
        y = 10

        Probe = XLSX2ATP.Probe(0, str(Torre + 1) + "R", str(Torre+1) + "G" + str(i+1)+ "-1", posx1-60, posy1)
        Level_object.append(Probe.ET)
        
        Probe = XLSX2ATP.Probe(0, str(Torre + 1) + "G" + str(i+1)+ "-2", str(Torre+2) + "R" , posx1+20, posy1)
        Level_object.append(Probe.ET)

    # se agrega el probador que va hacia la RPT.

    Probe = XLSX2ATP.Probe(270,Torre,Torre+1,posx1-80,posy1+20)
    Level_object.append(Probe.ET)


atp.xmlProject.append(Level_object)

#########################################################
#           Agregar Variables generales                 #
#########################################################

atp.funcChildObj(atp.xmlProject,"variables",{"NumSim":"1", "IOPCVP":"0"})

atp.funcCompileXML("ATP/" + "Version1",os.getcwd())