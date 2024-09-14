import tkinter as tk
from tkinter import font as tkfont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def iniciar_simulacion():
    # Obtener los valores de los campos de entrada
    Q_carbon_0 = float(entries["Cantidad inicial de carbón procesado (toneladas):"].get())
    P_grafeno_0 = float(entries["Precio inicial de venta del grafeno ($/kg):"].get())
    C_produccion_0 = float(entries["Costo inicial de producción de grafeno ($/kg):"].get())
    P_carbon = float(entries["Pureza del carbón (%):"].get())
    R_conv = float(entries["Rendimiento de conversión de carbón a grafeno (%):"].get())
    E = float(entries["Energía consumida por tonelada de carbón (kWh):"].get())
    P_energia = float(entries["Costo unitario de la energía (en $/kWh):"].get())
    C_operacion = float(entries["Costo fijo de operación anual ($):"].get())
    num_anios = int(entries["Ingrese el número de años en que desea proyectar la rentabilidad:"].get())
    anios = np.arange(0, num_anios + 1, 1)  # Período de tiempo (0 hasta num_anios)

    # Ecuaciones en función del tiempo
    Q_carbon = Q_carbon_0 * (1 + 0.15) ** anios  # Cantidad de carbón procesado
    P_grafeno = P_grafeno_0 * (1 + 0.05) ** anios  # Precio de venta del grafeno
    C_produccion = C_produccion_0 * (1 + 0.05) ** anios  # Costo de producción por kg de grafeno
    Q_grafeno = Q_carbon * (P_carbon/100) * (R_conv/100) * 1000  # Cantidad de grafeno producido (kg)

    # Ingresos y costos anuales
    Ingresos = Q_grafeno * P_grafeno
    Costos_energia = Q_carbon * E * P_energia
    Costos_produccion = (Q_grafeno * C_produccion) + Costos_energia + C_operacion

    # Retorno sobre la inversión (ROI)
    ROI = (Ingresos - Costos_produccion) / Costos_produccion

    # Limpiar la figura actual
    fig.clf()

    # Crear una nueva gráfica
    ax = fig.add_subplot(111)
    ax.plot(anios, ROI, marker='o', color='b', label='ROI')
    ax.set_title('Evolución del Retorno sobre la Inversión (ROI) en el Tiempo', fontsize=14)
    ax.set_xlabel('Años', fontsize=12)
    ax.set_ylabel('ROI', fontsize=12)
    ax.grid(True)
    ax.legend()
    ax.set_xticks(anios)

    # Ajustar el espacio para el título
    plt.tight_layout()

    # Dibujar la gráfica en el canvas
    canvas.draw()

    # Actualizar la información en la grilla
    labels = [
        f"Año {num_anios}:",
        f"Cantidad de carbón procesado: {Q_carbon[num_anios]:.2f} toneladas",
        f"Cantidad de grafeno producido: {Q_grafeno[num_anios]:.2f} kg",
        f"Ingresos: ${Ingresos[num_anios]:,.2f}",
        f"Costos de producción: ${Costos_produccion[num_anios]:,.2f}",
        f"ROI: {ROI[num_anios]:.2f} (o {ROI[num_anios] * 100:.2f}%)"
    ]

    for i, label_text in enumerate(labels):
        result_labels[i].config(text=label_text)

root = tk.Tk()
root.title("Simulación de Rentabilidad de Producción de Grafeno")

# Estilo de fuente
font_title = tkfont.Font(family="Helvetica", size=16, weight="bold")
font_label = tkfont.Font(family="Helvetica", size=12)
font_entry = tkfont.Font(family="Helvetica", size=12)
font_button = tkfont.Font(family="Helvetica", size=14, weight="bold")

# Estilo de fondo y colores
root.configure(bg="#f5f5f5")

# Crear un marco para los campos de entrada
frame_inputs = tk.Frame(root, bg="#ffffff", padx=10, pady=10, relief="raised", borderwidth=2)
frame_inputs.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# Crear un marco para la gráfica
frame_graph = tk.Frame(root, bg="#ffffff")
frame_graph.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

# Crear un marco para los resultados
frame_results = tk.Frame(root, bg="#ffffff")
frame_results.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

# Configurar el peso de las filas y columnas para que se expandan
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Etiqueta principal en la parte superior
label_title = tk.Label(frame_inputs, text="Simulación de Rentabilidad de Producción de Grafeno", font=font_title, bg="#ffffff")
label_title.grid(row=0, column=0, columnspan=2, pady=10)

variables = [
    ("Cantidad inicial de carbón procesado (toneladas):", 100),
    ("Precio inicial de venta del grafeno ($/kg):", 4176400),
    ("Costo inicial de producción de grafeno ($/kg):", 3000000),
    ("Pureza del carbón (%):", 50),
    ("Rendimiento de conversión de carbón a grafeno (%):", 10),
    ("Energía consumida por tonelada de carbón (kWh):", 1000),
    ("Costo unitario de la energía (en $/kWh):", 309),
    ("Costo fijo de operación anual ($):", 400000000),
    ("Ingrese el número de años en que desea proyectar la rentabilidad:", 20)
]

entries = {}
for i, (label_text, default_value) in enumerate(variables, start=1):
    tk.Label(frame_inputs, text=label_text, font=font_label, bg="#ffffff").grid(row=i, column=0, sticky="w")
    entry = tk.Entry(frame_inputs, font=font_entry, width=10)
    entry.insert(0, default_value)
    entry.grid(row=i, column=1, pady=5)
    entries[label_text] = entry

# Botón para iniciar la simulación
btn_iniciar = tk.Button(frame_inputs, text="Iniciar Simulación", command=iniciar_simulacion, font=font_button, bg="#007bff", fg="#ffffff", relief="raised")
btn_iniciar.grid(row=len(variables)+1, column=0, columnspan=2, pady=20, padx=20)

# Crear una figura y un canvas para Matplotlib
fig = plt.Figure(figsize=(8, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Crear etiquetas para mostrar los resultados
result_labels = []
for i in range(6):
    label = tk.Label(frame_results, text="", font=font_label, bg="#ffffff", anchor="w", justify="left")
    label.grid(row=i, column=0, sticky="ew")
    result_labels.append(label)

root.mainloop()
