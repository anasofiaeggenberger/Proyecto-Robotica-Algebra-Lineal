import numpy as np
import math

def rotation_matrix(theta):
    """
    Devuelve la matriz de rotación 2D para un ángulo dado (en radianes).
    R(theta) = [[cosθ, -sinθ],
                [sinθ,  cosθ]]
    """
    return np.array([
        [math.cos(theta), -math.sin(theta)],
        [math.sin(theta),  math.cos(theta)]
    ])

def translation_matrix(x, y):
    """
    Devuelve la matriz de traslación en coordenadas homogéneas.
    D(x, y) = [[1, 0, x],
               [0, 1, y],
               [0, 0, 1]]
    """
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ])