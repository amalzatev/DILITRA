import numpy as np

class Alignment:
    '''
    Clase para el alineamiento de la linea.
    '''

    def __init__(self, structures):
        self.inflection_points = self.get_inflection_points(structures)

    def get_inflection_points(self, structures):

        inflection_points = {}
        for structure in structures:

            inflection_points[structure.name] = np.array(
                [
                    structure.coordinates.get('x'),
                    structure.coordinates.get('y'),
                ]
            )
                
        return inflection_points
