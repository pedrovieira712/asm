from spade.agent import Agent
from .Behaviours.Sensor_Behav import *


class Sensor(Agent):
    def __init__(self, jid, password, id_lugar,  park_jid):
        super().__init__(jid, password)

        self.park_jid = park_jid
        self.id_lugar = id_lugar       
        self.is_free = True
        self.vehicle_id = None

    def print(self, txt):
        print(f"[SENSOR {self.tipo_sensor}] {txt}")

    async def setup(self):
        self.add_behaviour(RecvExitConfirmed())
        self.add_behaviour(RecvMarkSpot())
