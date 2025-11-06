import matplotlib.pyplot as plt
import matplotlib.animation as animation

def draw_robot(points, ax):
    xs, ys = zip(*points)
    ax.clear()

    ax.plot(xs, ys, '-o', linewidth=4, markersize=8, color='#0077ff')

    ax.plot(xs[-1], ys[-1], 'ro', markersize=10)
    ax.text(xs[-1] + 0.1, ys[-1] + 0.1, 'Efector final', color='red', fontsize=10)

    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_xlabel("Eje X", fontsize=10)
    ax.set_ylabel("Eje Y", fontsize=10)
    ax.set_title("Simulación de Brazo Robótico (Álgebra Lineal)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
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