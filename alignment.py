import numpy as np

class Alignment:
    '''
    Clase para el alineamiento de la linea.
    '''

    def __init__(self, structures):
        self.nodes = self.get_nodes(structures)

    def get_nodes(self, structures):

        nodes = {}
        for structure in structures:

            nodes[structure.name] = np.array(
                [
                    structure.coordinates.get('x'),
                    structure.coordinates.get('y'),
                ]
            )
                
        return nodes
    
    def is_the_last_node(self, node_name):
        '''
        Verifica si el nodo es el ultimo del alineamiento.
        
        args:
            -node_name (str): Nombre del nodo (estructura).
        
        return:
            (bool)
        '''
        
        node_names = list(self.nodes.keys())
        return node_name == node_names[-1]
    
    def align_point(self, point, node):
        '''
        Alinea un punto con respecto a la estructura especificada y direccion a la siguiente estrucutra si esta no es la ultima. En caso de que sea la ultima estructura, la direccion sera la estructura anterior.
        
        args:
            -point (numpy.ndarray): Coordenadas del punto.
            -node (str): Nombre de la estructura referencia.
        
        return:
            -point (numpy.ndarray): Coordenadas transformadas del punto.
        '''

        origin = self.nodes.get(node)

        nodes_names = list(self.nodes.keys())
        index = nodes_names.index(node)        
        if self.is_the_last_node(node):
            ref_structure_index = index - 1
        else:
            ref_structure_index = index + 1
        
        ref_strucutre_name = nodes_names[ref_structure_index]
        ref_strucutre_point = self.nodes.get(ref_strucutre_name)

        # Se trasladan los ejes
        point -= origin
        ref_strucutre_point -= origin 

        # Se rotan los ejes
        theta = np.arctan2(ref_strucutre_point[1], ref_strucutre_point[0]) - np.pi / 2
        
        rotation_matrix = np.array(
            [
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ]
        )

        point = np.dot(rotation_matrix, point)

        if self.is_the_last_node(node):
            point[0] = point[0] * -1
        
        return point
