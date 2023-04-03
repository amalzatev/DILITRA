import pandas as pd
import xml.etree.ElementTree as ET


class Header(object):
    def __init__(self):
        self.objHeader = ET.Element(
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
        
class Resistor(object):
    def __init__(self,index, row):
        posx = 140 + (100 + index * 120) % 2400
        posy = 180 + 300 * (1 + index // 20)
        self.auxET = ET.Element(
            "comp_content",
            attrib={
                "Angle": str(270),
                "PosX": str(posx),
                "PosY": str(posy),
                "Output": "1",
                "Icon": "default",
            },
        )
        ET.SubElement(
            self.auxET,
            "node",
            {
                "Name": "From",
                "Value": str(row["Nombre"]) + "R",
                "UserNamed": "true",
                "Kind": "1",
                "PosX": "-20",
                "PosY": "0",
                "NamePosX": "-4",
                "NamePosY": "0",
            },
        )

        ET.SubElement(
            self.auxET,
            "node",
            {
                "Name": "To",
                "Value": "      ",
                "UserNamed": "true",
                "Kind": "1",
                "PosX": "20",
                "PosY": "0",
                "NamePosX": "4",
                "NamePosY": "0",
                "Ground": "1",
            },
        )
        ET.SubElement(self.auxET, "data", {"Name": "", "Value": str(row["RPT"])})
        self.ET = ET.Element("comp", attrib={"Name": "RESISTOR"})
        self.ET.append(self.auxET)

class Probe(object):
    def __init__(self, ang, input, output, x, y):
        self.comp_content = ET.Element(
            "comp_content", attrib={"Angle": str(ang), "PosX": str(x), "PosY": str(y), "Icon": "default"}
        )
        self.comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "IN",
                    "Value": str(input),
                    "UserNamed": "true",
                    "Kind": "1",
                    "PosX": "-20",
                    "PosY": "0",
                    "NamePosX": "-4",
                    "NamePosY": "0",
                },
            )
        )
        self.comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT",
                    "Value": str(output),
                    "UserNamed": "true",
                    "Kind": "1",
                    "PosX": "20",
                    "PosY": "0",
                    "NamePosX": "4",
                    "NamePosY": "0",
                },
            )
        )
        self.comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "CURR",
                    "Value": "",
                    "Disabled": "true",
                    "Kind": "1",
                    "PosX": "0",
                    "PosY": "-10",
                    "NamePosX": "0",
                    "NamePosY": "-4",
                },
            )
        )
        for i in [1, 50, 0]:
            self.comp_content.append(
                ET.Element("data", attrib={"Name": "", "Value": str(i)})
            )
        self.probe = ET.Element(
            "probe",
            attrib={
                "CaptureSteadyState": "false",
                "OnScreen": "0",
                "ScreenFormat": "0",
                "ScreenShow": "0",
                "CurrNode": "false",
                "FontSize": "0",
                "Precision": "0",
                "TimeOnScreen": "false",
            },
        )
        self.probe.append(ET.Element("monitor", attrib={"Phase": "1"}))
        self.ET = ET.Element("comp", attrib={"Name": "PROBE_I"})
        self.ET.append(self.comp_content)
        self.ET.append(self.probe)

class Tower(object):

    def __init__(self, index, geometry, data, cable, nextrow):
        circuits = data["Circuitos"]
        ground = data["Ground"]
        posx = 200 + (100 + index * 120) % 2400
        posy = 100 + 300* (1 + index // 20)


        comp_content = ET.Element("comp_content",
            attrib={
                "PosX": str(posx),
                "PosY": str(posy),
                "NumPhases": str(3 * circuits + ground),
                "Icon": "default",
            },
            )

        circuit_name = {"0": "A", "1": "B"}
        DeltaY = -10
        Kind = 1

        for i in range(circuits):

            comp_content.append(
                ET.Element(
                    "node",
                    attrib={
                        "Name": "IN{}-{}".format(3 * i + 1, 3 * (i + 1)),
                        "Value": str(data["Nombre"]) + circuit_name[str(i)] + str(1),
                        "UserNamed": "true",
                        "NumPhases": "3",
                        "Kind": str(Kind),
                        "PosX": "-20",
                        "PosY": str(DeltaY),
                        "NamePosX": "-4",
                        "NamePosY": "-4",
                    },
                )
            )
            DeltaY += 10
            Kind += 1

        circuit_Ground = {"0": "GP", "1": "GS"}
        phNumber = circuits*3 + 1
        DeltaY = 10

        for i in range(ground):

            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "IN{}".format(phNumber + i),
                    "Value": str(data["Nombre"]) + circuit_Ground[str(i)] + str(1),
                    "UserNamed": "false",
                    "Kind": str(Kind),
                    "PosX": "-20",
                    "PosY": str(DeltaY),
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                    },
                )
            )
            DeltaY += 10
            Kind += 1

        phNumber += 1
        DeltaY = -10
        Kind = 1

        for i in range(circuits):
            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT{}-{}".format(3 * i + 1, 3 * (i + 1)),
                    "Value": str(data["Nombre"]) + circuit_name[str(i)] + str(2),
                    "UserNamed": "true",
                    "NumPhases": "3",
                    "Kind": str(Kind),
                    "PosX": "-20",
                    "PosY": str(DeltaY),
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                },
            )
            )
            DeltaY += 10
            Kind += 1
            
        phNumber = circuits*3 + 1
        DeltaY = 10

        for i in range(ground):
            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT{}".format(phNumber + i),
                    "Value": str(data["Nombre"]) + circuit_Ground[str(i)] + str(2),
                    "UserNamed": "false",
                    "Kind": "2",
                    "PosX": "-20",
                    "PosY": str(DeltaY),
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                },
            )
            )
            DeltaY += 10
            Kind += 1

        comp_content.append(
                ET.Element(
                "data", attrib={"Name": "Length", "Value": str(data["Longitud"])}
        )
        )
        comp_content.append(
        ET.Element("data", attrib={"Name": "Frequency", "Value": str(data["Frecuencia"])})
        )
        comp_content.append(
        ET.Element(
            "data",
            attrib={"Name": "Grnd resist", "Value": str(data["Resistividad"])},
        )
        )

        Comp_LCC = ET.Element("LCC",
            attrib={
            "NumPhases": str(phNumber + 1),
            "LineCablePipe": "1",
            "ModelType": "1",
        },
        )
        line_header = ET.SubElement(
            Comp_LCC,
            "line_header",
            {
            "RealMtrx": "false",
            "SkinEffect": "true",
            "AutoBundle": "true",
            "MetricUnit": "true",
            },
            )

        for i in range(phNumber+1):
            geometryFase = geometry["Fase" + str(i+1)]
            line_header.append(
                ET.Element("line",
                    attrib={
                    "PhNo":str(i+1),
                    "Rin":str(0),
                    "Rout":str(cable["Diametro"] / 2),
                    "Resis":str(cable["Resistencia DC"]),
                    "React":str(cable["Reactancia"]),
                    "Horiz":str(geometryFase[0]),
                    "Vtow":str(geometryFase[1]),
                    "Vmid":str(geometryFase[2]),
                    "NB":str(geometryFase[3]),
                    "Separ":str(data["Separacion conductores"]),
                    "Alpha":str(data["Angulo"]),
                    },
                    )
                )



        self.ET = ET.Element("comp", attrib={"Name":"LCC", "Id": str(index+1)})

        self.ET.append(comp_content)
        self.ET.append(Comp_LCC)

class Conn(object):

    def __init__(self,NumPhases,X1,Y1,X2,Y2):
        self.ET = ET.Element("conn")
        ET.SubElement(self.ET,"conn_content", attrib={"NumPhases":str(NumPhases), "Pos1X":str(X1), "Pos1Y":str(Y1), "Pos2X":str(X2), "Pos2Y":str(Y2)})
