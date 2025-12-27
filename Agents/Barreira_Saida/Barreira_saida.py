from spade.agent import Agent
from .behaviours.BS_behaviours import *


class BarreiraSaida(Agent):
    
    def __init__(self, jid, password, park_jid):
        super().__init__(jid, password)
        self.park_jid = park_jid    
           
    async def setup(self):
        self.add_behaviour(ReceiveExitRequest())
        self.add_behaviour(ReceivePaymentConfirmation())
    
    
        
        