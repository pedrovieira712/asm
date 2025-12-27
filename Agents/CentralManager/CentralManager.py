from spade.agent import Agent
from .Behaviours.Cm_Behav import *

class CentralManager(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.parking_spots = {}
        self.redirect_requests = {}
        
    def print(self, txt):
        print(f"[CENTRAL_MANAGER] {txt}")
    
    async def setup(self):
        self.add_behaviour(ReceiveRedirectRequestsBehaviour())
        self.add_behaviour(ReceiveNextParkInfoBehaviour())
        self.add_behaviour(ReceiveAvailabilityResponseBehaviour())
    
    def get_parking_spots(self):
        return self.parking_spots
    
    def set_parking_spots(self, parking_spots):
        self.parking_spots = parking_spots
    
    def add_parking_spot(self, park_jid, location):
        self.parking_spots[park_jid] = location
    
    def remove_parking_spot(self, park_jid):
        if park_jid in self.parking_spots:
            del self.parking_spots[park_jid]

    def get_redirect_requests(self):
        return self.redirect_requests
    
    def set_redirect_requests(self, redirect_requests):
        self.redirect_requests = redirect_requests
    
    def add_redirect_request(self, vehicle_id, vehicle_info):
        self.redirect_requests[vehicle_id] = vehicle_info
    
    def remove_redirect_request(self, vehicle_id):
        if vehicle_id in self.redirect_requests:
            del self.redirect_requests[vehicle_id]
    