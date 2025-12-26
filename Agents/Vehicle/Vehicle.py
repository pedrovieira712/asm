from spade.agent import Agent

from Vehicle.Behaviours.Vc_behav import *

class Vehicle(Agent):
    
    def __init__(self, jid, password, vehicle_type, user_type):
        super().__init__(jid, password)
        
        self.vehicle_type = vehicle_type
        self.user_type = user_type
        self.plate = None
    
    async def setup(self):
        print(f"Vehicle Agent {self.jid} starting.")

        send_forwarding_request_behav = SendFowardingRequestBehaviour()
        self.add_behaviour(send_forwarding_request_behav)

        receive_forwarding_response_behav = ReceiveFowardingResponseBehaviour()
        self.add_behaviour(receive_forwarding_response_behav)
    
    def get_vehicle_type(self):
        return self.vehicle_type
    
    def set_vehicle_type(self, vehicle_type):
        self.vehicle_type = vehicle_type
    
    def get_user_type(self):
        return self.user_type
    
    def set_user_type(self, user_type):
        self.user_type = user_type
    
    def get_plate(self):
        return self.plate
    
    def set_plate(self, plate):
        self.plate = plate
        
        
        