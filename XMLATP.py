# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:57:09 2019

@author: ctovar
"""
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom


class XMLFILE:
    floatTimeStep = float()
    floatTmax = float()
    intXOPT = int()
    intCOPT = int()
    intTopLefX = 10000
    intTopLefY = 10000
    dictHeater = dict()
    strXMLfile = str()

    def funcProjecCreate(self):
        self.xmlProject = ET.Element("project")
        self.xmlProject.set("Application", "ATPDraw")
        self.xmlProject.set("Version", "7")
        self.xmlProject.set("VersionXML", "1")
        #ET.SubElement(self.xmlProject, "header", self.dictHeater)
        #ET.SubElement(self.xmlProject, "objects", self.dictHeater)

    def funcCompileXML(self, strNameXML, strdir):
        path = os.path.join(strdir, strNameXML)

        self.strXMLfile = minidom.parseString(ET.tostring(self.xmlProject)).toprettyxml(
            indent="   "
        )
        doc = open(path + ".xml", "w")
        doc.write(self.strXMLfile)
        doc.close()

    def funcChildObj(self, xmlparent, strchild, dicAtrib):
        self.XMLObj = ET.SubElement(xmlparent, strchild, dicAtrib)

    def funcChildComp(self, dicAtrib):
        self.XMLComp = ET.SubElement(self.XMLObj, "comp", dicAtrib)

    def funcChildContent(self, dicAtrib):
        self.XMLContent = ET.SubElement(self.XMLComp, "comp_content", dicAtrib)

    def funcChildNodes(self, dicAtrib):
        ET.SubElement(self.XMLContent, "node", dicAtrib)

    def funcChilddata(self, dicAtrib):
        ET.SubElement(self.XMLContent, "data", dicAtrib)

    def funcChildLCC(self, dicAtrib):
        self.xmlLCC = ET.SubElement(self.XMLComp, "LCC", dicAtrib)

    def funcChildHLCC(self, dicAtrib):
        self.xmlLCCH = ET.SubElement(self.xmlLCC, "line_header", dicAtrib)

    def funcChildLine(self, dicAtrib):
        ET.SubElement(self.xmlLCCH, "line", dicAtrib)

    def funcChildVaria(self, dicAtrib):
        ET.SubElement(self.xmlProject, "variables", dicAtrib)

    def funcChildRes(self, dicAtrib):
        self.xmlRes = ET.SubElement(self.XMLObj, "comp", dicAtrib)

    def funcChildConRes(self, dicAtrib):
        self.xmlConRes = ET.SubElement(self.xmlRes, "comp_content", dicAtrib)

    def funcChildNodeRes(self, dicAtrib):
        ET.SubElement(self.xmlConRes, "node", dicAtrib)

    def funcChildDataRes(self, dicAtrib):
        ET.SubElement(self.xmlConRes, "data", dicAtrib)

    def funcChildProbe(self, dicAtrib):
        self.xmlProbe = ET.SubElement(self.XMLObj, "comp", dicAtrib)

    def funcChildConProbe(self, dicAtrib):
        self.xmlConProbe = ET.SubElement(self.xmlProbe, "comp_content", dicAtrib)

    def funcChildNodeProbe(self, dicAtrib):
        ET.SubElement(self.xmlConProbe, "node", dicAtrib)

    def funcChildDataProbe(self, dicAtrib):
        ET.SubElement(self.xmlConProbe, "data", dicAtrib)

    def funcChildProbeProbe(self, dicAtrib):
        self.xmlProbeProbe = ET.SubElement(self.xmlProbe, "probe", dicAtrib)

    def funcChildMonitorProbe(self, dicAtrib):
        ET.SubElement(self.xmlProbeProbe, "monitor", dicAtrib)

    def funcChildConn(self, dicAtrib):
        self.xmlConn = ET.SubElement(self.XMLObj, "conn", dicAtrib)

    def funcChildConConn(self, dicAtrib):
        ET.SubElement(self.xmlConn, "conn_content", dicAtrib)


