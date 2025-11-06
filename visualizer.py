import matplotlib.pyplot as plt
import matplotlib.animation as animation

def draw_robot(points, ax):
    """
    Dibuja el brazo robótico a partir de una lista de puntos [(x0,y0), ..., (xn,yn)].
    """
    xs, ys = zip(*points)
    ax.clear()
    ax.plot(xs, ys, '-o', linewidth=3, markersize=8, color='royalblue')
    ax.set_xlim(-sum([abs(x) for x in xs]) - 1, sum([abs(x) for x in xs]) + 1)
    ax.set_ylim(-sum([abs(y) for y in ys]) - 1, sum([abs(y) for y in ys]) + 1)
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_title("Simulación del Brazo Robótico (Álgebra Lineal)")
    ax.grid(True)
    ax.set_aspect('equal')

def animate_robot(arm, sequence):
    """
    Anima el brazo robótico según una secuencia de ángulos.
    :param arm: objeto RobotArm
    :param sequence: lista de listas de ángulos en grados, ej. [[0,0], [10,20], [20,40], ...]
    """
    fig, ax = plt.subplots()
    def update(frame):
        arm.set_angles(sequence[frame])
        points = arm.forward_kinematics()
        draw_robot(points, ax)

    ani = animation.FuncAnimation(fig, update, frames=len(sequence), interval=300)
    plt.show()