from robot_arm import RobotArm
from visualizer import animate_robot

if __name__ == "__main__":
    print("=== Simulación de Brazo Robótico con Transformaciones Lineales ===")

    # Definir longitudes de los eslabones
    lengths = [3, 2, 1]  
    arm = RobotArm(lengths)

    # Definir secuencia de ángulos para la animación
    sequence = [
        [0, 0, 0],
        [15, 10, 5],
        [30, 20, 10],
        [45, 30, 15],
        [60, 45, 25],
        [75, 60, 35],
        [90, 75, 45],
    ]

    animate_robot(arm, sequence)