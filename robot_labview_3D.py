import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from robot_arm import RobotArm

# === MATRICES DE ROTACIÓN 3D ===
def Rz(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])

def Ry(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def Rx(theta):
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta),  np.cos(theta)]
    ])

def animate_robot_3D():
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(121, projection='3d')
    ax_text = fig.add_subplot(122)
    plt.subplots_adjust(wspace=0.25)

    # --- BRAZO ROBÓTICO ---
    lengths = [2.5, 2.0, 1.5]
    frames = 160
    angles_sequence = [
        [np.sin(t/25)*90, np.cos(t/20)*60, np.sin(t/30)*45]
        for t in range(frames)
    ]

    # --- Estética 3D ---
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-2, 6)
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_zlabel("Eje Z")
    ax.set_title("Brazo Robótico 3D — Cinemática Directa con Álgebra Lineal", pad=15)
    ax.view_init(elev=25, azim=35)

    # --- Panel matemático ---
    ax_text.set_facecolor((0.03, 0.03, 0.05, 0.9))
    for s in ax_text.spines:
        ax_text.spines[s].set_color('#6CF1FF')
        ax_text.spines[s].set_linewidth(2)
    ax_text.axis('off')
    text_display = ax_text.text(0.02, 0.98, "", color='white', va='top',
                                family='monospace', fontsize=10, wrap=True)

    line, = ax.plot([], [], [], '-o', lw=3, color='#00d0ff', markersize=8)
    trail, = ax.plot([], [], [], color='gold', lw=1.5, alpha=0.6)

    trail_x, trail_y, trail_z = [], [], []

    def update(frame):
        angles = np.deg2rad(angles_sequence[frame])
        theta1, theta2, theta3 = angles

        # --- MATRICES DE ROTACIÓN COMPUESTAS ---
        R_total = Rz(theta1) @ Ry(theta2) @ Rx(theta3)
        p1 = Rz(theta1) @ np.array([lengths[0], 0, 0])
        p2 = Rz(theta1) @ Ry(theta2) @ np.array([lengths[1], 0, 0]) + p1
        p3 = R_total @ np.array([lengths[2], 0, 0]) + p2

        # --- Dibujar brazo ---
        xs = [0, p1[0], p2[0], p3[0]]
        ys = [0, p1[1], p2[1], p3[1]]
        zs = [0, p1[2], p2[2], p3[2]]
        line.set_data(xs, ys)
        line.set_3d_properties(zs)

        trail_x.append(p3[0])
        trail_y.append(p3[1])
        trail_z.append(p3[2])
        trail.set_data(trail_x, trail_y)
        trail.set_3d_properties(trail_z)

        # --- Mostrar cálculos matemáticos ---
        R1 = np.round(Rz(theta1), 3)
        R2 = np.round(Ry(theta2), 3)
        R3 = np.round(Rx(theta3), 3)

        matrices_text = (
            "=== MATRICES DE ROTACIÓN 3D ===\n\n"
            f"Rz(θ1={np.rad2deg(theta1):.1f}°):\n{R1}\n\n"
            f"Ry(θ2={np.rad2deg(theta2):.1f}°):\n{R2}\n\n"
            f"Rx(θ3={np.rad2deg(theta3):.1f}°):\n{R3}\n\n"
            f"Posición final del efector:\n({p3[0]:.2f}, {p3[1]:.2f}, {p3[2]:.2f})"
        )

        text_display.set_text(matrices_text)

        # También mostrar en la terminal
        print("\n========================== FRAME", frame, "==========================")
        print(matrices_text)

        return line, trail, text_display

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
    plt.show()

if __name__ == "__main__":
    animate_robot_3D()