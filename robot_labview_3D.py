import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patheffects as path_effects
from mpl_toolkits.mplot3d import Axes3D

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

def analyze_frame(frame, angles_sequence, lengths):
    """Realiza los cálculos algebraicos de un frame específico"""
    angles_deg = angles_sequence[frame]
    theta1, theta2, theta3 = np.deg2rad(angles_deg)

    R1, R2, R3 = Rz(theta1), Ry(theta2), Rx(theta3)
    R_total = R1 @ R2 @ R3

    det_R = np.linalg.det(R_total)
    inv_R = np.linalg.inv(R_total)
    rango = np.linalg.matrix_rank(R_total)
    nullidad = 3 - rango
    independencia = "Sí ✔" if rango == 3 else "No ✘"

    base_col = R_total.T
    base_row = R_total
    p3 = R_total @ np.array([lengths[2], 0, 0])
    T = np.block([
        [R_total, p3.reshape(3, 1)],
        [np.zeros((1, 3)), np.ones((1, 1))]
    ])

    text = (
        f"=== ANÁLISIS MATEMÁTICO — Frame {frame} ===\n\n"
        f"Ángulos (°): θ1={angles_deg[0]:.1f}, θ2={angles_deg[1]:.1f}, θ3={angles_deg[2]:.1f}\n\n"
        f"R_total:\n{np.round(R_total,3)}\n\n"
        f"Determinante = {det_R:.4f} {'✔ Invertible' if det_R != 0 else '✘ No invertible'}\n\n"
        f"Rango = {rango}, Nullidad = {nullidad}\n"
        f"Columnas linealmente independientes: {independencia}\n\n"
        f"Base columna:\n{np.round(base_col,3)}\n\n"
        f"Base fila:\n{np.round(base_row,3)}\n\n"
        f"Inversa:\n{np.round(inv_R,3)}\n\n"
        f"Matriz homogénea T:\n{np.round(T,3)}"
    )

    return text, R_total

    text = (
        f"=== ANÁLISIS MATEMÁTICO — Frame {frame} ===\n\n"
        f"Ángulos (°): θ1={angles_deg[0]:.1f}, θ2={angles_deg[1]:.1f}, θ3={angles_deg[2]:.1f}\n\n"
        f"R_total:\n{np.round(R_total,3)}\n\n"
        f"Determinante = {det_R:.4f} {'✅ Invertible' if det_R != 0 else '❌ No invertible'}\n\n"
        f"Rango = {rango}, Nullidad = {nullidad}\n"
        f"Columnas linealmente independientes: {independencia}\n\n"
        f"Base columna:\n{np.round(base_col,3)}\n\n"
        f"Base fila:\n{np.round(base_row,3)}\n\n"
        f"Inversa:\n{np.round(inv_R,3)}\n\n"
        f"Matriz homogénea T:\n{np.round(T,3)}"
    )

    return text, R_total


def animate_robot_3D():
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(11.5, 7))
    ax = fig.add_subplot(121, projection="3d")
    ax_text = fig.add_subplot(122)
    plt.subplots_adjust(wspace=0.3)

    # --- CONFIGURACIÓN DEL BRAZO ---
    lengths = [2.5, 2.0, 1.5]
    frames = 361  # 0 a 360 grados exactos
    angles_sequence = [
        [t, np.sin(t / 30) * 60, np.cos(t / 25) * 45]
        for t in np.linspace(0, 360, frames, endpoint=True)
    ]

    # --- CONFIGURACIÓN VISUAL ---
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-2, 6)
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_zlabel("Eje Z")
    title = ax.set_title(
    "Brazo Robótico 3D",
    pad=15,
    fontsize=13,
    color="#00CFFF",
    fontweight="bold",
)
    title.set_path_effects([
    path_effects.Stroke(linewidth=4, foreground="#02121A"),  # “aura” detrás
    path_effects.Normal()
])
    ax.view_init(elev=25, azim=35)  # fija, estable
    ax.grid(True, linestyle="--", alpha=0.2)
    ax.set_facecolor("#050608")

    # --- ELEMENTOS VISUALES ---
    line, = ax.plot([], [], [], "-o", lw=3, color="#00CFFF", markersize=8)
    trail, = ax.plot([], [], [], color="white", lw=1.5, alpha=0.7)
    effector_point = None

    # --- PANEL DERECHO ---
    ax_text.set_facecolor((0.03, 0.04, 0.08, 0.9))
    for s in ax_text.spines:
        ax_text.spines[s].set_color("#00CFFF")
        ax_text.spines[s].set_linewidth(2)
    ax_text.axis("off")
    text_display = ax_text.text(
        0.02, 0.98, "", color="white", va="top",
        family="monospace", fontsize=10, wrap=True
    )

    trail_x, trail_y, trail_z = [], [], []

    # --- FUNCIÓN DE ANIMACIÓN ---
    def update(frame):
        nonlocal effector_point
        angles = np.deg2rad(angles_sequence[frame])
        theta1, theta2, theta3 = angles

        R_total = Rz(theta1) @ Ry(theta2) @ Rx(theta3)
        p1 = Rz(theta1) @ np.array([lengths[0], 0, 0])
        p2 = Rz(theta1) @ Ry(theta2) @ np.array([lengths[1], 0, 0]) + p1
        p3 = R_total @ np.array([lengths[2], 0, 0]) + p2

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

        if effector_point:
            effector_point.remove()
        effector_point = ax.scatter(
            p3[0], p3[1], p3[2],
            color="#FF3131", s=70, edgecolor="white", linewidth=0.8
        )

        text_display.set_text(f"Frame {frame}\nÁngulos (°): {np.round(angles_sequence[frame], 1)}")

        if frame == frames - 1:
            ani.event_source.stop()
            print("\n✅ Simulación completada.")
            frame_input = int(input("Ingresa el número de frame (0–360) que deseas analizar: "))
            text, _ = analyze_frame(frame_input, angles_sequence, lengths)
            print("\n" + text + "\n")
            text_display.set_text(text)
            print("\n🟢 La ventana permanecerá abierta hasta que la cierres manualmente.\n")
            plt.show(block=True)

        return line, trail, text_display, effector_point

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=35, blit=False)
    plt.show(block=True)


if __name__ == "__main__":
    animate_robot_3D()