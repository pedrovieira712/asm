from spade.agent import Agent
from Utils.agent_logger import create_park_manager_logger
from .Behaviours.Mp_behav import *

class ManagerParque(Agent):
    def __init__(self, jid, password, park_id, capacity, max_height, location):
        super().__init__(jid, password)

        self.logger = create_park_manager_logger(park_id)

        self.park_id = park_id
        self.capacity = capacity
        self.max_height = max_height
        self.location = location
        self.occupied_spots = 0

        self.parking_spots = {}
        self.parking_spots_info = {}
        self.spot_sensors = {}
        self.paymetns_record = {}
        self.sensor_vehicles = {}
        self.entry_times = {}
        self.vehicle_parking_spots = {}

        self.vehicle_types = ["car", "motorcycle", "truck", "caravan", "bus"]
        self.user_types = ["normal", "pregnant", "reduced_mobility", "elderly"]

    
    async def setup(self):
        self.add_behaviour(ReceiveRedirectVehicleRequestBehaviour())
        self.add_behaviour(ReceiveEntryRequestBehaviour())
        self.add_behaviour(ReceivePaymentConfirmationBehaviour())
        self.add_behaviour(ReceivePaymentVerificationBehaviour())
        self.add_behaviour(ReceiveEntrytimeRequestBehaviour())

    def is_valid_request(self, vehicle_type, user_type):
        return (
            vehicle_type in self.vehicle_types and
            user_type in self.user_types
        )
    
    def check_availability(self, vehicle_type, user_type, vehicle_height):
        if not self.is_valid_request(vehicle_type, user_type):
            return False

        if self.occupied_spots >= self.capacity:
            return False

        if vehicle_height is not None and vehicle_height > self.max_height:
            return False

        for spot_id, is_occupied in self.parking_spots.items():
            if is_occupied:
                continue

            spot_info = self.parking_spots_info.get(spot_id, {})

            allowed_vehicle_types = spot_info.get("allowed_vehicle_types")
            if allowed_vehicle_types and vehicle_type not in allowed_vehicle_types:
                continue

            allowed_user_types = spot_info.get("allowed_user_types")
            if allowed_user_types and user_type not in allowed_user_types:
                continue

            return True

        return False

    
    def get_free_spot(self, vehicle_type, user_type):
        for spot_id, is_occupied in self.parking_spots.items():
            if is_occupied:
                continue

            spot_info = self.parking_spots_info.get(spot_id, {})

            allowed_vehicle_types = spot_info.get("allowed_vehicle_types")
            if allowed_vehicle_types and vehicle_type not in allowed_vehicle_types:
                continue

            allowed_user_types = spot_info.get("allowed_user_types")
            if allowed_user_types and user_type not in allowed_user_types:
                continue

            return spot_id

        return None
    
    def mark_spot_occupied(self, spot_id):
        if spot_id in self.parking_spots and not self.parking_spots[spot_id]:
            self.parking_spots[spot_id] = True
            self.occupied_spots += 1
    
    def mark_spot_free(self, spot_id):
        if spot_id in self.parking_spots and self.parking_spots[spot_id]:
            self.parking_spots[spot_id] = False
            self.occupied_spots -= 1
    
    def add_parking_spot(self, spot_id, allowed_vehicle_types=None, allowed_user_types=None):
        self.parking_spots[spot_id] = False
        self.parking_spots_info[spot_id] = {
            "allowed_vehicle_types": allowed_vehicle_types,
            "allowed_user_types": allowed_user_types
        }

    def remove_parking_spot(self, spot_id):
        if spot_id not in self.parking_spots:
            return

        if self.parking_spots.get(spot_id, False):
            self.occupied_spots -= 1

        del self.parking_spots[spot_id]

        if spot_id in self.parking_spots_info:
            del self.parking_spots_info[spot_id]

        if spot_id in self.spot_sensors:
            del self.spot_sensors[spot_id]
    
    def add_sensor_for_spot(self, spot_id, sensor_jid):
        self.spot_sensors[spot_id] = sensor_jid
    
    def remove_sensor_for_spot(self, spot_id):
        if spot_id in self.spot_sensors:
            del self.spot_sensors[spot_id]

    def get_sensor_for_spot(self, spot_id):
        return self.spot_sensors.get(spot_id)
    
    def record_payment(self, vehicle_id, boolean):
        self.paymetns_record[vehicle_id] = boolean
    
    def has_paid(self, vehicle_id):
        return self.paymetns_record.get(vehicle_id, False)
    
    def rem_payment_record(self, vehicle_id):
        if vehicle_id in self.paymetns_record:
            del self.paymetns_record[vehicle_id]

    def associate_vehicle_with_sensor(self, vehicle_id, sensor_jid):
        self.sensor_vehicles[vehicle_id] = sensor_jid
    
    def get_sensor_for_vehicle(self, vehicle_id):
        return self.sensor_vehicles.get(vehicle_id)
    
    def rem_sensor_for_vehicle(self, vehicle_id):
        if vehicle_id in self.sensor_vehicles:
            del self.sensor_vehicles[vehicle_id]
    
    def record_entry_time(self, vehicle_id, entry_time):
        self.entry_times[vehicle_id] = entry_time

    def get_entry_time(self, vehicle_id):
        return self.entry_times.get(vehicle_id)
    
    def rem_entry_time(self, vehicle_id):
        if vehicle_id in self.entry_times:
            del self.entry_times[vehicle_id]

    def associate_vehicle_with_spot(self, vehicle_id, spot_id):
        self.vehicle_parking_spots[vehicle_id] = spot_id
    
    def get_vehicle_spot(self, vehicle_id):
        return self.vehicle_parking_spots.get(vehicle_id)
    
    def rem_vehicle_spot_association(self, vehicle_id):
        if vehicle_id in self.vehicle_parking_spots:  
            del self.vehicle_parking_spots[vehicle_id]
    
    
    
