from spade.agent import Agent

from CentralManager.Behaviours.Cm_Behav import *

class CentralManager(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        
        self.vehicle_types = [
            "carro",
            "moto",
            "camiao",
            "caravana",
            "autocarro"
        ]
        
        self.vehicle_heights = {
            "carro": 1.5,
            "moto": 1.0,
            "camiao": 3.5,
            "caravana": 2.8,
            "autocarro": 3.2
        }
        
        self.user_types = [
            "normal",
            "grávida",
            "mobilidade_reduzida",
            "idoso",
            "veículo_elétrico"
        ]

        self.vehicles = []
        self.parking_spots = []
    
    async def setup(self):
        self.print("Central Manager started")
        
        recv_forwarding_behav = RecvForwarding()
        self.add_behaviour(recv_forwarding_behav)
        
        send_parking_spot_request_behav = SendParkingSpotRequest()
        self.add_behaviour(send_parking_spot_request_behav)
        
        recv_next_parking_spot_behav = RecvNextParkingSpot()
        self.add_behaviour(recv_next_parking_spot_behav)
        
        send_parking_spot_approval_behav = SendParkingSpotAproval()
        self.add_behaviour(send_parking_spot_approval_behav)
        
        recv_parking_spot_approval_behav = RecvParkingSpotAproval()
        self.add_behaviour(recv_parking_spot_approval_behav)
        
        send_update_parking_spot_info_behav = SendUpdateParkingSpotInfo()
        self.add_behaviour(send_update_parking_spot_info_behav)
    
    def get_vehicles(self):
        return self.vehicles
    
    def get_parking_spots(self):
        return self.parking_spots
    
    def set_vehicles(self, vehicles):
        self.vehicles = vehicles
    
    def set_parking_spots(self, parking_spots):
        self.parking_spots = parking_spots
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_parking_spot(self, parking_spot):
        self.parking_spots.append(parking_spot)
    
    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)

    def remove_parking_spot(self, parking_spot):
        self.parking_spots.remove(parking_spot)