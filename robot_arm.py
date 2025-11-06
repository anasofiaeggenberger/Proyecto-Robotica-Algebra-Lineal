import numpy as np
from robot_math import rotation_matrix

class RobotArm:
    """
    Clase que representa un brazo robótico plano compuesto por varios eslabones.
    Cada eslabón se define por su longitud y un ángulo de rotación.
    """

    def __init__(self, lengths):
        """
        Inicializa el brazo robótico.
        :param lengths: Lista con las longitudes de los eslabones [L1, L2, ...]
        """
        self.lengths = lengths
        self.angles = [0 for _ in lengths]  # Inicialmente todos los ángulos en 0

    def set_angles(self, angles_deg):
        """
        Establece los ángulos del brazo en grados.
        """
        self.angles = [np.deg2rad(a) for a in angles_deg]

    def forward_kinematics(self):
        """
        Calcula las posiciones (x, y) de cada articulación y del efector final.
        Retorna una lista de coordenadas [(x0,y0), (x1,y1), ..., (xn,yn)]
        """
        points = [(0, 0)]  # Base del brazo
        x, y, total_angle = 0, 0, 0

        for i, (L, theta) in enumerate(zip(self.lengths, self.angles)):
            total_angle += theta
            x += L * np.cos(total_angle)
            y += L * np.sin(total_angle)
            points.append((x, y))

        return points

    def show_transformations(self):
        """
        Muestra paso a paso las matrices de rotación y los puntos calculados.
        """
        print("\n=== MATRICES DE TRANSFORMACIÓN Y POSICIONES ===")
        x, y, total_angle = 0, 0, 0

        for i, (L, theta) in enumerate(zip(self.lengths, self.angles), start=1):
            total_angle += theta
            R = np.array([
                [np.cos(total_angle), -np.sin(total_angle)],
                [np.sin(total_angle),  np.cos(total_angle)]
            ])
            x += L * np.cos(total_angle)
            y += L * np.sin(total_angle)

            print(f"\n→ Articulación {i}")
            print("Ángulo acumulado:", np.rad2deg(total_angle))
            print("Matriz de rotación:")
            print(np.round(R, 3))
            print(f"Posición final parcial: ({x:.2f}, {y:.2f})")

        print("\nPosición final del efector:", (round(x, 2), round(y, 2)))
        print("==============================================")