from random import random
from spade.agent import Agent
import math

from .Behaviours.Loc_Behav import *

class Location(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.park_locations = {}
    
    def print(self, txt):
        print(f"[LOCATION] {txt}")
    
    async def setup(self):
        self.add_behaviour(RecvRequestsLocation())

    def get_closest_park(self, current_location):
        if not self.park_locations:
            return None

        closest_park = None
        min_distance = float("inf")

        for park_jid, park_location in self.park_locations.items():
            distance = abs(current_location - park_location)
            
            if distance < min_distance:
                min_distance = distance
                closest_park = park_jid

        return closest_park

    def get_park_locations(self):
        return self.park_locations

    def set_park_locations(self, park_locations):
        self.park_locations = park_locations

    def add_ParkLocation(self, park_id, location):
        self.park_locations[park_id] = location

    def remove_ParkLocation(self, park_id):
        if park_id in self.park_locations:
            del self.park_locations[park_id]    