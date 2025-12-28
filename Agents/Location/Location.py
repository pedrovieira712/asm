from random import random
from spade.agent import Agent
import math

from .Behaviours.Loc_Behav import *

class Location(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.park_locations = {}
    
    async def setup(self):
        self.add_behaviour(RecvRequestsLocation())

    def haversine(self, coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        R = 6371.0 

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def get_closest_park(self, current_location, tried_parks=None):
        if tried_parks is None:
            tried_parks = set()

        if not self.park_locations:
            return None
        available_parks = {
            park_jid: park_location
            for park_jid, park_location in self.park_locations.items()
            if park_location not in tried_parks
        }

        if not available_parks:
            return None
        
        closest_park = min(
            available_parks.keys(),
            key=lambda jid: self.haversine(current_location, available_parks[jid])
        )

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