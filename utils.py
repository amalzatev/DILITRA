import numpy as np

def calculate_vector(point1, point2):
    '''
    Crea un vector dado dos puntos.
    
    args:
        -point1(numpy.ndarray): Primer punto. Arreglo de numeros decimales con las coordenadas.
        -point2(numpy.ndarray): Segundo punto. Arreglo de numeros decimales con las coordenadas.
    
    return:
        -(numpy.ndarray): Vector resultante. Arreglo de numeros decimales con las coordenadas.
    '''

    return np.array([point2[0] - point1[0], point2[1] - point1[1]])

def calculate_angle_two_vector(vector1, vector2):
    '''
    Devuelve al angulo entre dos vectores.
    
    args:
        -vector1(numpy.ndarray): Primer vector. Arreglo de numeros decimales con las coordenadas.
        -vector2(numpy.ndarray): Segundo vector. Arreglo de numeros decimales con las coordenadas.
    
    return:
        -(numpy.ndarray): Angulo en radianes.
        '''

    unit_vector_1 = calculate_unit_vector(vector1)
    unit_vector_2 = calculate_unit_vector(vector2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return np.arccos(dot_product)

def calculate_unit_vector(vector):
    '''
    Calcula el vector unitario de un vector.

    arg:
    -vector(numpy.ndarray): Vector al que se le calculara el vector unitario. Arreglo de numeros decimales con las coordenadas.

    return:
    -(numpy.ndarray): Vector unitario resultado. Arreglo de numeros decimales con las coordenadas.
    '''

    return  vector / np.linalg.norm(vector)
