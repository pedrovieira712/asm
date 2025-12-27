from spade.agent import Agent
import asyncio
from datetime import datetime
from .Behaviours.Behav_Kiosque_Entrada import *

class Kiosque_Entrada(Agent):    
    def __init__(self, jid, password, park_jid):
        super().__init__(jid, password)
        self.park_jid = park_jid
        self.vehicles_waiting = {}
        self.vehicles = {}  
        
    def print(self, txt):
        print(f"[KIOSQUE_ENTRADA {self.park_jid}] {txt}")
        
    async def setup(self):
        self.add_behaviour(RecvEntryRequest())
        self.add_behaviour(RecvEntryResponse())
    
    def mark_vehicle_waiting(self, vehicle_id):
        self.vehicles_waiting[vehicle_id] = True
    
    def unmark_vehicle_waiting(self, vehicle_id):
        if vehicle_id in self.vehicles_waiting:
            del self.vehicles_waiting[vehicle_id]
    
    def is_vehicle_waiting(self, vehicle_id):
        return self.vehicles_waiting.get(vehicle_id, False)
    
    def register_vehicle(self, vehicle_id, vehicle_jid):
        self.vehicles[vehicle_id] = vehicle_jid
    
    def get_vehicle_jid(self, vehicle_id):
        return self.vehicles.get(vehicle_id, None)
    
    def unregister_vehicle(self, vehicle_id):
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]
