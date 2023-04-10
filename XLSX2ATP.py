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
    def __init__(self,index, row, posx, posy):
        """

        Esta clase crea el componente para las resistencias de puesta a tierra, en donde se debe indicar:

            -->index = Numero de elemento o torre que se va a crear.
            -->row = Resistencias de puesta a tierra correspondiente a cada torre.
            -->posx = posicion de la resistencia en x en ATP.
            -->posy = posicion de la resistencia en y en ATP.

        """


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
                "Value": str(index+1) + "RPT",
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
        ET.SubElement(self.auxET, "data", {"Name": "", "Value": str(row)})
        self.ET = ET.Element("comp", attrib={"Name": "RESISTOR"})
        self.ET.append(self.auxET)

class Probe(object):
    """
    
    Esta es una clase para crear los probadores de corriente.

        -->ang = Angulo del elemento en ATP.
        -->input = Cual es el nombre que se se colocara al punto de entrada del elemento.
        -->output = Cual es el nombre que se se colocara al punto de salida del elemento.
        -->posx = posicion del elemento en x en ATP.
        -->posy = posicion del elemento en y en ATP.
    
    Nota:  no se hace el numbramiento de los nodos desde acá, ya que cada caso de conexión es particular.

    """
    def __init__(self, ang, input, output, posx, posy):
        self.comp_content = ET.Element(
            "comp_content", attrib={"Angle": str(ang), "PosX": str(posx), "PosY": str(posy), "Icon": "default"}
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

    """
    
    Esta es una clase para crear los probadores de corriente.

        -->index = Numero de elemento o torre que se va a crear.
        -->geometry = Geometria de cada torre.
        -->data = Datos generales del alineamiento.
        -->cable = Información de los conductores utilizados.
        -->posx = posicion del elemento en x en ATP.
        -->posy = posicion del elemento en y en ATP.
    
    """

    def __init__(self, index, geometry, data, cable, posx, posy):
        circuits = data["Circuitos"]
        ground = data["Ground"]
        Vano = data["Longitud"]

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
                        "Value": str(index+1) + circuit_name[str(i)] + str(1),
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

        circuit_Ground = {"0": "G1-", "1": "G2-"}
        phNumber = circuits*3 + 1
        DeltaY = 10

        for i in range(ground):

            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "IN{}".format(phNumber + i),
                    "Value": str(index+1)+ circuit_Ground[str(i)] + str(1),
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
                    "Value": str(index+1)+ circuit_name[str(i)] + str(2),
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
            
        phNumber = circuits*3 + ground
        DeltaY = 10

        for i in range(ground):
            comp_content.append(
            ET.Element(
                "node",
                attrib={
                    "Name": "OUT{}".format(phNumber + i),
                    "Value": str(index+1) + circuit_Ground[str(i)] + str(2),
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
                "data", attrib={"Name": "Length", "Value": str(Vano[index])}
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
            "NumPhases": str(phNumber),
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

        cont = 1
        for i in range(circuits):

            for j in range (3):

                geometryFase = geometry["C" + str(i+1) + "-" + str(j+1)]
                Cond = cable["C" + str(i+1)]

                line_header.append(
                    ET.Element("line",
                        attrib={
                        "PhNo":str(cont),
                        "Rin":str(0),
                        "Rout":str(Cond["Diametro"] / 2),
                        "Resis":str(Cond["Resistencia DC"]),
                        "React":str(Cond["Reactancia"]),
                        "Horiz":str(geometryFase["Horiz"]),
                        "Vtow":str(geometryFase["Vtow"]),
                        "Vmid":str(geometryFase["Vmid"]),
                        "NB":str(data["NB"]),
                        "Separ":str(data["Separacion conductores"]),
                        "Alpha":str(data["Angulo"]),
                        },
                        )
                    )
                cont += 1
        
        for i in range(ground):

            geometryFase = geometry["CG" + str(i+1) + "-" + str(1)]
            Cond = cable["CG" + str(i+1)]
            line_header.append(
                ET.Element("line",
                    attrib={
                    "PhNo":str(cont),
                    "Rin":str(0),
                    "Rout":str(Cond["Diametro"] / 2),
                    "Resis":str(Cond["Resistencia DC"]),
                    "React":str(Cond["Reactancia"]),
                    "Horiz":str(geometryFase["Horiz"]),
                    "Vtow":str(geometryFase["Vtow"]),
                    "Vmid":str(geometryFase["Vmid"]),
                    "NB":str(data["NB"]),
                    "Separ":str(data["Separacion conductores"]),
                    "Alpha":str(data["Angulo"]),
                    },
                    )
                )
            cont += 1


        self.ET = ET.Element("comp", attrib={"Name":"LCC", "Id": str(index+1)})

        self.ET.append(comp_content)
        self.ET.append(Comp_LCC)

class Conn(object):

    def __init__(self,NumPhases,posx1,posy1,posx2,posy2):
        self.ET = ET.Element("conn")
        ET.SubElement(self.ET,"conn_content", attrib={"NumPhases":str(NumPhases), "Pos1X":str(posx1), "Pos1Y":str(posy1), "Pos2X":str(posx2), "Pos2Y":str(posy2)})
