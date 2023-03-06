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
    def __init__(self, posx, posy, row):
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
    def __init__(self, input, output, x, y):
        self.comp_content = ET.Element(
            "comp_content", attrib={"PosX": str(x), "PosY": str(y), "Icon": "default"}
        )
        self.comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "IN",
                    "Value": input,
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
                    "Value": output,
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
        posy = 100 + 100 * (1 + index // 20)


        comp_content = ET.Element("comp_content",
            attrib={
                "PosX": str(posx),
                "PosY": str(posy),
                "NumPhases": str(3 * circuits + ground),
                "Icon": "default",
            },
            )

        circuit_name = {"0": "A", "1": "B"}
        for i in range(circuits):
            comp_content.append(
                ET.Element(
                    "node",
                    attrib={
                        "Name": "IN{}-{}".format(3 * i + 1, 3 * (i + 1)),
                        "Value": str(data["Nombre"]) + circuit_name[str(i)],
                        "UserNamed": "true",
                        "NumPhases": "3",
                        "Kind": "1",
                        "PosX": "-20",
                        "PosY": "-10",
                        "NamePosX": "-4",
                        "NamePosY": "-4",
                    },
                )
        )

        phNumber = circuits*3 + 1

        for i in range(ground):

            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "IN{}".format(phNumber + i),
                    "Value": "",
                    "UserNamed": "false",
                    "Kind": "2",
                    "PosX": "-20",
                    "PosY": "-10",
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                },
            )
        )


        phNumber += 1

        for i in range(circuits):
            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT{}-{}".format(3 * i + 1, 3 * (i + 1)),
                    "Value": nextrow + circuit_name[str(i)],
                    "UserNamed": "true",
                    "NumPhases": "3",
                    "Kind": "1",
                    "PosX": "-20",
                    "PosY": "-10",
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                },
            )
        )
            
        phNumber = circuits*3 + 1

        for i in range(ground):
            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT{}".format(phNumber + i),
                    "Value": "",
                    "UserNamed": "false",
                    "Kind": "2",
                    "PosX": "-20",
                    "PosY": "-10",
                    "NamePosX": "-4",
                    "NamePosY": "-4",
                },
            )
        )


        

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
            line_header.append(
                ET.Element("line",
                    attrib={
                    "PhNo":str(i+1),
                    "Rin":str(0),
                    "Rout":str(cable["Diametro"] / 2),
                    "React":str(0),
                    "Resis":str(cable["Resistencia DC"]),
                    "Horiz":str(geometry["Horiz"]),
                    "Vtow":str(geometry["Vtow"]),
                    "Vmid":str(geometry["Vmid"]),
                    "NB":str(geometry["NB"]),
                    "Separ":str(data["Separacion conductores"]),
                    "Alpha":str(data["Angulo"]),
                    },
                    )
                )



        self.ET = ET.Element("comp", attrib={"Name":"LCC", "Id": "1"})

        self.ET.append(comp_content)
        self.ET.append(Comp_LCC)
