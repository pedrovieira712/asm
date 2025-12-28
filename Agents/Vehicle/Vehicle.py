from spade.agent import Agent

from .Behaviours.Vc_behav import *

class Vehicle(Agent):
    
    def __init__(self, jid, password, vehicle_type, user_type, location, redirect, vehicle_height, plate, skip_payment):
        super().__init__(jid, password)
        
        self.vehicle_type = vehicle_type
        self.user_type = user_type
        self.vehicle_height = vehicle_height
        self.plate = plate
        self.location = location
        self.prefers_redirect = redirect
        self.is_waiting = False
        self.is_parked = False
        self.skip_payment = skip_payment
    
    async def setup(self):
        self.add_behaviour(SendEntryRequestBehaviour())
        self.add_behaviour(RecvEntryDecision())
        self.add_behaviour(RecvRedirectResponse())
        self.add_behaviour(RecvPaymentAmount())
        self.add_behaviour(RecvPaymentWarning())
        self.add_behaviour(VehicleRetryEntryRequestBehaviour(period=10))
        self.add_behaviour(ReceiveCanExitResponse())
        self.add_behaviour(RecvPaymentConfirmation())
        self.add_behaviour(ReceiveRedirectDenial())
    
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

    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location

    def get_vehicle_height(self):
        return self.vehicle_height
    
    def set_vehicle_height(self, height):
        self.vehicle_height = height

    def set_waiting(self, waiting):
        self.is_waiting = waiting
    
    def is_waiting_at_park(self):
        return self.is_waiting
    
    def set_parked(self, parked):  
        self.is_parked = parked
    
    def is_currently_parked(self):
        return self.is_parked
    
    def is_skipping_payment_process(self):
        return self.skip_payment
    
    def set_payment_skipping(self, skip):
        self.skip_payment = skip

    

        
        
        