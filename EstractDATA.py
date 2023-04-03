import pandas as pd
from READXML.ReadFileXML import ReadXML
import numpy as np
import XMLATP
import XLSX2ATP
import pandas as pd
import xml.etree.ElementTree as ET
import os



# Se estraen los datos con la funcion ReadFileXML de tal manera que se pueden tener acceso a cualquiera las
# tablas que se obtienen desde el PLS Cadd

data = ReadXML('PLC/SM_1x220kV_LasDamas_Portezuelos.xml')
Summary = data.Dicc_Final
Tables = data.List_Table
St_Coordinates = data.ExtracData('Structure_Coordinates_Report')
St_Att_Coordinates = data.ExtracData('Structure_Attachment_Coordinates')
CPh_Definitions = data.ExtracData('Circuit_and_Phase_Definitions_and_Labels')
Retention_start = CPh_Definitions["start_structure"]
Retention_end = CPh_Definitions["end_structure"]

Retentions = list(set(Retention_start))

Guarda = {"X":[], "Z":[]}
Geometry = {"Structures":[], "Phase1":[], "Phase2":[], "Phase3":[],
         'HeightPhase1':[], 'HeightPhase2':[], 'HeightPhase3':[]}

for i in Retention_end:
     if i not in Retentions:
          Retentions.append(i)

for i in range(len(St_Coordinates)):

    Structure = St_Coordinates.iloc[i]["struct_number"]
    Data_Str = St_Att_Coordinates[St_Att_Coordinates["struct_number"] == Structure]

    for Fila in range(len(Data_Str)):
        
        Z_ins = Data_Str.iloc[Fila]["insulator_attach_point_z"]
        Z_wire = Data_Str.iloc[Fila]["wire_attach_point_z"]
        x1_x2 = float(St_Coordinates.iloc[i]["x"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_x"])
        y1_y2 = float(St_Coordinates.iloc[i]["y"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_y"])
        z1_z2 = float(St_Coordinates.iloc[i]["z"]) - float(Data_Str.iloc[Fila]["insulator_attach_point_z"])

        if Z_ins == Z_wire:
            
            Guarda["X"].append(np.sqrt(x1_x2**2 + y1_y2**2))
            Guarda["Z"].append(np.round(np.abs(z1_z2),2))

        else:

            X = np.round(np.sqrt(x1_x2**2 + y1_y2**2), 2)
            X1 = -X if (x1_x2 < 0) else X

            Geometry["Phase" + Data_Str.iloc[Fila]["phase_no"]].append(np.round(X1))
            Geometry["Height" + "Phase" + Data_Str.iloc[Fila]["phase_no"]].append(np.round(np.abs(z1_z2),2))

    Geometry["Structures"].append(Structure)


Data_Frame = pd.DataFrame(Geometry)

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

#############################################################
#     Datos Para Resistencias de Puesta a tierra           ##
#############################################################

R = pd.DataFrame({"Nombre":["Nombre 1","Nombre 2"],"RPT":[20, 20]})

data_RPT = {"Nombre":list(St_Coordinates["struct_number"]),"RPT": 0.5,
            "PosX":[], "PosY":[]}

Level_object = ET.Element("objects",{})

for Torre in range(len(data_RPT["Nombre"])):

    dic1 = XLSX2ATP.Resistor(Torre,R.iloc[0])
    Level_object.append(dic1.ET)


atp.xmlProject.append(Level_object)

#############################################################
#                     Datos Para LCC                       ##
#############################################################

index = 1
geometrys = {"Torre1":{"Fase1":[-11.761802583, 59.06, 59.06, 4],
                      "Fase2":[-9.748487062, 47.56, 47.56, 4],
                      "Fase3":[-17.220002904, 47.56, 47.56, 4],
                      "Fase4":[12.115213576, 58.97, 58.97, 4],
                      "Fase5":[10.053377542, 47.56, 47.56, 4],
                      "Fase6":[17.601775479, 47.56, 47.56, 4],
                      "Fase7":[-10.474082299, 63.06, 35.62, 4],
                      "Fase8":[10.474082299, 62.98, 35.39, 4]}} #Horiz="-11.761802583" Vtow="59.06" Vmid="59.06" NB="4"

geometry = geometrys["Torre1"]


data = {"Resistividad":100,"RPT": 0.5}

General_Data = {"Longitud": 0.55, "Resistividad":100,
        "Separacion conductores": 0.5, "Angulo" :45,
        "Circuitos": 2, "Ground": 2, "Nombre": 1, "Frecuencia": 60}


cable = {"Diametro": 1.265*2, "Resistencia DC": 0.0833, "Reactancia":0.5169}
nextrow = "2"

for Torre in range(len(data_RPT["Nombre"])):

    LCC1 = XLSX2ATP.Tower(Torre,geometry,General_Data,cable,nextrow)
    Level_object.append(LCC1.ET)

atp.xmlProject.append(Level_object)

#############################################################
#                     Agregar conectores                   ##
#############################################################



for Torre in range(len(data_RPT["Nombre"])):
    y = 0
    for i in range(2):
        
        posx1 = 220 + (100 + Torre * 120) % 2400
        posy1 = 90 + 300 * (1 + Torre // 20) + y
        posx2 = posx1 +  80
        posy2 = posy1
        y = 10
        CONN = XLSX2ATP.Conn(3,posx1,posy1,posx2,posy2)
        Level_object.append(CONN.ET)

    y = 0
    for i in range(2):
        
        posx1 = 220 + (100 + Torre * 120) % 2400
        posy1 = 110 + 300 * (1 + Torre // 20) + y
        posx2 = posx1 +  10
        posy2 = posy1
        y = 10
        # CONN = XLSX2ATP.Conn(1,posx1,posy1,posx2,posy2)
        # Level_object.append(CONN.ET)
    
        Probe = XLSX2ATP.Probe(0,Torre,Torre+1,posx1+20,posy1)
        Level_object.append(Probe.ET)

        Probe = XLSX2ATP.Probe(0,Torre,Torre+1,posx1-60,posy1)
        Level_object.append(Probe.ET)
    
        
    posx1 = 220 + (100 + Torre * 120) % 2400
    posy1 = 110 + 300 * (1 + Torre // 20) + y
    posx2 = posx1 +  10
    posy2 = posy1
    y = 10
    # CONN = XLSX2ATP.Conn(1,posx1,posy1,posx2,posy2)
    # Level_object.append(CONN.ET)

    Probe = XLSX2ATP.Probe(270,Torre,Torre+1,posx1-80,posy1+20)
    Level_object.append(Probe.ET)

      


atp.xmlProject.append(Level_object)

#########################################################
#           Agregar Variables generales                 #
#########################################################

atp.funcChildObj(atp.xmlProject,"variables",{"NumSim":"1", "IOPCVP":"0"})

atp.funcCompileXML("ATP/" + "Version1",os.getcwd())

#print(data_RPT)


