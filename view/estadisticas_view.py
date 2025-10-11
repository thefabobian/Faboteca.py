import tkinter as tk
from tkinter import ttk
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EstadisticasView:
    def __init__(self, master, controlador):
        self.master = master
        self.controlador = controlador
        self.master.title("📈 Estadísticas de Préstamos - Faboteca")
        self.master.geometry("950x700")
        self.master.configure(bg="#f7f8fa")

        ttk.Label(master, text="📊 Estadísticas Generales", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Frame botones
        frame_botones = ttk.Frame(master)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="📚 Libros más prestados", command=self.grafico_libros).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="👥 Usuarios con más préstamos", command=self.grafico_usuarios).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="⏰ Usuarios con más vencimientos", command=self.grafico_vencidos).grid(row=0, column=2, padx=10)

        # Área para gráfico
        self.frame_grafico = ttk.Frame(master)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

    # === FUNCIONES DE GRÁFICOS ===
    def limpiar_grafico(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

    def grafico_libros(self):
        self.limpiar_grafico()
        prestamos = self.controlador.listar_prestamos()
        contador_libros = Counter()

        for p in prestamos:
            for l in p.get("libros", []):
                contador_libros[l["titulo"]] += l.get("cantidad", 1)

        if not contador_libros:
            ttk.Label(self.frame_grafico, text="No hay datos disponibles").pack()
            return

        libros, cantidades = zip(*contador_libros.most_common(10))

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(libros, cantidades, color="#3b82f6")
        ax.set_title("📚 Libros más prestados", fontsize=14, pad=15)
        ax.set_xlabel("Título del libro")
        ax.set_ylabel("Cantidad de préstamos")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def grafico_usuarios(self):
        self.limpiar_grafico()
        prestamos = self.controlador.listar_prestamos()
        contador_usuarios = Counter(p["usuario"] for p in prestamos)

        if not contador_usuarios:
            ttk.Label(self.frame_grafico, text="No hay datos disponibles").pack()
            return

        usuarios, cantidades = zip(*contador_usuarios.most_common(8))
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(cantidades, labels=usuarios, autopct="%1.1f%%", startangle=90)
        ax.set_title("👥 Usuarios con más préstamos", fontsize=14, pad=10)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def grafico_vencidos(self):
        self.limpiar_grafico()
        prestamos = self.controlador.listar_prestamos()
        contador_vencidos = Counter()
        hoy = datetime.today().date()

        for p in prestamos:
            fecha_dev = datetime.strptime(p["fecha_devolucion"], "%Y-%m-%d").date()
            if fecha_dev < hoy:
                contador_vencidos[p["usuario"]] += 1

        if not contador_vencidos:
            ttk.Label(self.frame_grafico, text="No hay préstamos vencidos").pack()
            return

        usuarios, cantidades = zip(*contador_vencidos.most_common(10))

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(usuarios, cantidades, color="#ef4444")
        ax.set_title("⏰ Usuarios con más préstamos vencidos", fontsize=14, pad=15)
        ax.set_xlabel("Cantidad de préstamos vencidos")
        ax.invert_yaxis()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
