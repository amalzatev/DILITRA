'''
Clases de los objetos usados por ATPDraw
'''

import xml.etree.ElementTree as ET

class Resistor:
    '''
    Clase para el objeto resistencia de ATPDraw.

    Atributos:
        resistance (float): La resistencia del elemento.
        x_pos (int): Coordenada en x en el lienzo de ATPDraw.
        y_pos (int): Coordenada en y en el lienzo de ATPDraw.
    '''
    
    
    def __init__(self, resistance, x_pos, y_pos):
        self.resistance = resistance
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def create_xml_element(self):
        '''
        
        '''
    
