import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from robot_arm import RobotArm

def rotation_matrix(theta):
    """Devuelve la matriz de rotación 2D"""
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

def animate_robot_labview():
    """Simulación con panel de matrices en tiempo real"""
    plt.style.use('dark_background')

    # --- FIGURA PRINCIPAL CON DOS SUBPLOTS ---
    fig, (ax_robot, ax_text) = plt.subplots(1, 2, figsize=(11, 6))
    plt.subplots_adjust(wspace=0.35)

    # --- CONFIGURAR BRAZO ROBÓTICO ---
    lengths = [3, 2, 1]
    arm = RobotArm(lengths)
    frames = 160
    angles_sequence = [
        [np.sin(t / 20) * 60, np.cos(t / 25) * 45, np.sin(t / 30) * 30]
        for t in range(frames)
    ]

    # --- GRÁFICA IZQUIERDA: BRAZO ROBÓTICO ---
    points = arm.forward_kinematics()
    xs, ys = zip(*points)
    line, = ax_robot.plot(xs, ys, '-o', lw=4, color='#00b3ff', markersize=8)
    effector, = ax_robot.plot([xs[-1]], [ys[-1]], 'ro', markersize=10)
    trail, = ax_robot.plot([], [], color='orange', lw=1.5, alpha=0.6)

    ax_robot.set_xlim(-7, 7)
    ax_robot.set_ylim(-7, 7)
    ax_robot.set_title("Simulación del Brazo Robótico", fontsize=13, pad=15)
    ax_robot.set_xlabel("Eje X")
    ax_robot.set_ylabel("Eje Y")
    ax_robot.grid(True, linestyle='--', alpha=0.3)
    ax_robot.set_aspect('equal')

    # --- Panel derecho con estilo visual ---
    ax_text.set_facecolor((0.05, 0.05, 0.08, 0.8))  # fondo oscuro semitransparente
    for side in ax_text.spines:
        ax_text.spines[side].set_color('#00b3ff')
        ax_text.spines[side].set_linewidth(2)

    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    ax_text.set_xticks([])
    ax_text.set_yticks([])

    text_display = ax_text.text(
        0.02, 0.98, "", fontsize=10, color='white', va='top',
        family='monospace', wrap=True
    )

    trajectory_x, trajectory_y = [], []

    # --- FUNCIÓN DE ACTUALIZACIÓN ---
    def update(frame):
        angles = angles_sequence[frame]
        arm.set_angles(angles)
        points = arm.forward_kinematics()
        xs, ys = zip(*points)

        # Dibujar brazo
        line.set_data(xs, ys)
        if len(xs) == 0 or len(ys) == 0:
            return line, effector, trail, text_display
        effector.set_data([xs[-1]], [ys[-1]])

        # Rastro del efector final
        trajectory_x.append(xs[-1])
        trajectory_y.append(ys[-1])
        trail.set_data(trajectory_x, trajectory_y)

        # --- Calcular y mostrar matrices en panel derecho ---
        matrices_text = "=== MATRICES DE ROTACIÓN ===\n"
        total_angle = 0
        x, y = 0, 0
        for i, (L, theta_deg) in enumerate(zip(arm.lengths, angles), start=1):
            theta_rad = np.deg2rad(theta_deg)
            total_angle += theta_rad
            R = rotation_matrix(total_angle)
            matrices_text += f"\nR{i} (Ángulo acumulado {np.rad2deg(total_angle):.1f}°):\n"
            matrices_text += np.array2string(np.round(R, 3), separator=', ') + "\n"
            x += L * np.cos(total_angle)
            y += L * np.sin(total_angle)
            matrices_text += f"Coordenada parcial {i}: ({x:.2f}, {y:.2f})\n"

        matrices_text += "\nPosición final del efector:\n"
        matrices_text += f"({x:.2f}, {y:.2f})"

        # Actualizar texto visual
        text_display.set_text(matrices_text)

        return line, effector, trail, text_display

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
    plt.show()

if __name__ == "__main__":
    animate_robot_labview()