from robot_arm import RobotArm
from visualizer import animate_robot

if __name__ == "__main__":
    print("=== Simulación de Brazo Robótico con Transformaciones Lineales ===")

    # Longitudes de los eslabones
    lengths = [3, 2, 1]
    arm = RobotArm(lengths)

    # Definir una secuencia de ángulos (en grados)
    sequence = [
        [0, 0, 0],
        [20, 10, 5],
        [40, 20, 10],
        [60, 40, 20],
        [80, 50, 30],
        [100, 70, 45]
    ]

    # Mostrar los cálculos para la última posición
    arm.set_angles(sequence[-1])
    arm.show_transformations()

    # Animar todo el movimiento
    animate_robot(arm, sequence)