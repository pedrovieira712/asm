from random import random
from spade.agent import Agent

from Location.Behaviours.Loc_Behav import *

class Location(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.park_locations = {}
    
    def print(self, txt):
        print(f"[LOCATION] {txt}")
    
    async def setup(self):
        self.print("Location Agent started")
        
        recv_requests_behav = RecvRequestsLocation()
        self.add_behaviour(recv_requests_behav)
        
        send_location_info_behav = SendLocationInfo()
        self.add_behaviour(send_location_info_behav)

    def get_park_locations(self):
        return self.park_locations

    def set_park_locations(self, park_locations):
        self.park_locations = park_locations

    def add_ParkLocation(self, park_id, location):
        self.park_locations[park_id] = location

    def remove_ParkLocation(self, park_id):
        if park_id in self.park_locations:
            del self.park_locations[park_id]    