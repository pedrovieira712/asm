# Sensor/Behaviours/Sensor_Behav.py
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime, timedelta


class AtualizarEstadoSensor(CyclicBehaviour):
    """
    Recebe mensagens do ManagerParque e atualiza o estado do sensor.

    Diagrama 'Entrada Disponível':
        Manager -> Sensor : 'Lugar Livre'

    Diagramas 'Saída' / 'Multa':
        Manager -> Sensor : 'Livre' / 'Sensor Livre'
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        tipo_msg = msg.metadata.get("tipo")
        sensor = self.agent

        if tipo_msg == "LUGAR_LIVRE":
            # Manager indica que este lugar foi reservado / está pronto a ser ocupado
            sensor.estado = "RESERVADO"
            sensor.print(f"[Sensor {sensor.id_lugar}] Estado -> RESERVADO (Lugar Livre)")

            # Guardamos timestamp para possível simulação
            sensor._hora_reserva = datetime.now()

        elif tipo_msg in ("LIVRE", "SENSOR_LIVRE"):
            # Manager indica que o lugar / saída voltou a estar livre
            sensor.estado = "LIVRE"
            sensor.print(f"[Sensor {sensor.id_lugar}] Estado -> LIVRE")

        # Podes adicionar outros comandos aqui se for preciso


class SimularOcupacaoLugar(CyclicBehaviour):
    """
    Simula a transição 'Ocupa Lugar' do diagrama de Entrada Disponível.

    Ideia:
      - Depois de o Manager mandar 'LUGAR_LIVRE' (estado RESERVADO),
        passado algum tempo assumimos que o veículo chegou ao lugar.
      - O sensor muda o estado para 'OCUPADO'.

    (Aqui não enviamos mensagem de volta ao Manager, porque
     nos teus diagramas essa seta não existe; é só mudança interna.)
    """

    async def run(self):
        sensor = self.agent

        # Se não for sensor de lugar, não faz nada
        if sensor.tipo_sensor != "LUGAR":
            await self.sleep(1)
            return

        # Só faz sentido se estivermos em estado RESERVADO
        if getattr(sensor, "_hora_reserva", None) and sensor.estado == "RESERVADO":
            agora = datetime.now()
            # Por exemplo, passado 5 segundos consideramos que o carro estacionou
            if agora - sensor._hora_reserva > timedelta(seconds=5):
                sensor.estado = "OCUPADO"
                sensor.print(f"[Sensor {sensor.id_lugar}] Estado -> OCUPADO (Ocupa Lugar)")
                # Apagamos a hora de reserva para não voltar a entrar
                sensor._hora_reserva = None

        await self.sleep(1)
