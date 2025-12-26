# Sensor/__init__.py
from spade.agent import Agent
from Sensor.Behaviours.Sensor_Behav import (
    AtualizarEstadoSensor,
    SimularOcupacaoLugar,
)


class Sensor(Agent):
    """
    Agente Sensor

    Pode representar:
        - um sensor de LUGAR (dentro do parque)
        - um sensor de SAIDA (na barreira de saída)

    Nos teus diagramas:
        - Entrada Disponível: Manager Parque -> Sensor : 'Lugar Livre'
                              Sensor (interno) : 'Ocupa Lugar'
        - Saída / Multa:      Manager -> Sensor : 'Livre' / 'Sensor Livre'
    """

    def __init__(self, jid, password, tipo_sensor, id_lugar=None):
        """
        :param tipo_sensor: 'LUGAR' ou 'SAIDA'
        :param id_lugar:    id do lugar associado (se for sensor de lugar)
        """
        super().__init__(jid, password)

        self.tipo_sensor = tipo_sensor      # 'LUGAR' ou 'SAIDA'
        self.id_lugar = id_lugar           # só faz sentido se for LUGAR

        # Estado simples do sensor
        #  - 'LIVRE'     : nada detetado
        #  - 'RESERVADO' : Manager disse que o lugar está livre para um veículo
        #  - 'OCUPADO'   : veículo detetado (Ocupa Lugar)
        self.estado = "LIVRE"

    def print(self, txt):
        print(f"[SENSOR {self.tipo_sensor}] {txt}")

    async def setup(self):
        self.print(f"Sensor [{self.tipo_sensor}] iniciado. Lugar: {self.id_lugar}")

        # Recebe comandos do ManagerParque (Lugar Livre / Livre / Sensor Livre)
        self.add_behaviour(AtualizarEstadoSensor())

        # Se for sensor de lugar, podemos simular a ocupação depois de 'Lugar Livre'
        if self.tipo_sensor == "LUGAR":
            self.add_behaviour(SimularOcupacaoLugar())
