import tkinter as tk
from tkinter import ttk

LOGS = []


def logs_color(text, color):
    LOGS.insert(0, (text, color))


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")


class GUI:

    def __init__(self, agents):
        self.root = tk.Tk()
        self.root.title("Sistema Multi-Agente – Parque")
        self.root.geometry("1500x850")

        self.agents = agents

        # listas por tipo
        self.central = []
        self.kentrada = []
        self.ksaida = []
        self.barreira = []
        self.manager = []
        self.location = []
        self.sensores = []
        self.veiculos = []
        self.espera = []

        # labels
        self.labels = {
            "central": [],
            "kentrada": [],
            "ksaida": [],
            "barreira": [],
            "manager": [],
            "location": [],
            "sensor": [],
            "vehicle": [],
            "espera": []
        }

        col = 0

        def make_frame(width):
            frame = ScrollableFrame(self.root, width=width, height=800,
                                    relief=tk.RAISED, borderwidth=2)
            frame.grid(column=len(self.frames), row=0, padx=5, pady=5)
            return frame

        self.frames = {
            "central": make_frame(220),
            "manager": make_frame(220),
            "kentrada": make_frame(220),
            "ksaida": make_frame(220),
            "barreira": make_frame(220),
            "location": make_frame(220),
            "sensor": make_frame(220),
            "vehicle": make_frame(220),
            "espera": make_frame(220),
        }

        for a in agents:
            n = a.__class__.__name__

            if n == "CentralManager":
                self.central.append(a)
            elif n == "Kiosque_Entrada":
                self.kentrada.append(a)
            elif n == "Kiosque_saida":
                self.ksaida.append(a)
            elif n == "BarreiraSaida":
                self.barreira.append(a)
            elif n == "ManagerParque":
                self.manager.append(a)
            elif n == "Location":
                self.location.append(a)
            elif n == "Sensor":
                self.sensores.append(a)
            elif n == "Vehicle":
                self.veiculos.append(a)
            elif n == "ZonadeEspera":
                self.espera.append(a)

        def build(group, key):
            for ag in group:
                if hasattr(ag, "create_display"):
                    labels = ag.create_display(self.frames[key])
                    self.labels[key].append(labels)

        build(self.central, "central")
        build(self.manager, "manager")
        build(self.kentrada, "kentrada")
        build(self.ksaida, "ksaida")
        build(self.barreira, "barreira")
        build(self.location, "location")
        build(self.sensores, "sensor")
        build(self.veiculos, "vehicle")
        build(self.espera, "espera")

        self.update_loop()

    def update_loop(self):

        def upd(group, lab_list):
            for i, ag in enumerate(group):
                if hasattr(ag, "update_display"):
                    ag.update_display(lab_list[i])

        upd(self.central, self.labels["central"])
        upd(self.manager, self.labels["manager"])
        upd(self.kentrada, self.labels["kentrada"])
        upd(self.ksaida, self.labels["ksaida"])
        upd(self.barreira, self.labels["barreira"])
        upd(self.location, self.labels["location"])
        upd(self.sensores, self.labels["sensor"])
        upd(self.veiculos, self.labels["vehicle"])
        upd(self.espera, self.labels["espera"])

        self.root.after(1000, self.update_loop)