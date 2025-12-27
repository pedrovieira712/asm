from spade.agent import Agent
from .Behaviours.behaviours import *


class ZonadeEspera(Agent):
    def __init__(self, jid, password, park_jid):
        super().__init__(jid, password)
        self.wait_vehicles = []
        self.park_jid = park_jid


    async def setup(self):
        self.add_behaviour(VehicleWaitingRequest())
        self.add_behaviour(VehicleWaitingRequestExit())

    def add_waiting_vehicle(self, vehicle_id):
        self.wait_vehicles.append(vehicle_id)

    def remove_waiting_vehicle(self, vehicle_id):
        if vehicle_id in self.wait_vehicles:
            self.wait_vehicles.remove(vehicle_id) 

