import XLSX2ATP
import XMLATP
import pandas as pd
import xml.etree.ElementTree as ET
import os


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

#########################################################
#            Datos Para un solo elemento                #
#########################################################

R = pd.DataFrame({"Nombre":["Nombre 1","Nombre 2"],"RPT":[20, 20]})

#########################################################
#           Agregar Header desde XLSX2ATP               #
#########################################################

Level_object = ET.Element("objects",{})

#########################################################
#            Agregar elemento Resitencia                #
#########################################################

dic1 = XLSX2ATP.Resistor(490,280,R.iloc[0])

Level_object.append(dic1.ET)

#########################################################
#            Agregar elemento probe                     #
#########################################################

probe1 = XLSX2ATP.Probe("4R","XX0004", 40-90+20,2820)
Level_object.append(probe1.ET)
#atp.xmlProject.append(Level_object)

#########################################################
#            Agregar elemento LCC                       #
#########################################################

index = 1
geometry = {"Horiz": 20, "Vtow": 10, "Vmid": 2, "NB": 4}

data = {"Resistividad":100,"RPT": 0.5}

General_Data = {"Longitud": 0.55, "Resistividad":100,
        "Separacion conductores": 0.5, "Angulo" :45,
        "Circuitos": 2, "Ground": 2, "Nombre": 1, "Frecuencia": 60}


cable = {"Diametro": 1.265*2, "Resistencia DC": 0.0833, "Reactancia":0.5169}
nextrow = "2"


LCC1 = XLSX2ATP.Tower(index,geometry,General_Data,cable,nextrow)

Level_object.append(LCC1.ET)
atp.xmlProject.append(Level_object)

#########################################################
#           Agregar Variables generales                 #
#########################################################

atp.funcChildObj(atp.xmlProject,"variables",{"NumSim":"1", "IOPCVP":"0"})

atp.funcCompileXML("ATP/" + "Version1",os.getcwd())