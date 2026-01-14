from spade.agent import Agent
from Utils.agent_logger import create_barrier_logger
from Config import Config as cfg
from .behaviours.BS_behaviours import *


class BarreiraSaida(Agent):
    
    def __init__(self, jid, password, park_jid):
        super().__init__(jid, password)
        
        park_id = cfg.get_jid_name(park_jid).replace("park_manager_", "")
        self.logger = create_barrier_logger(park_id)
        
        self.park_jid = park_jid    
           
    async def setup(self):
        self.add_behaviour(ReceiveExitRequest())
        self.add_behaviour(ReceivePaymentConfirmation())
    
    
        
        