from spade.agent import Agent
import asyncio
from datetime import datetime
from Utils.agent_logger import create_kiosk_exit_logger
from .Behaviours.Behav_Kiosque_Saida import *
from Config import Config as cfg

class Kiosque_saida(Agent):
    def __init__(self, jid, password, park_jid, tarifa_minuto, hora_fecho, multa_fixa):
        super().__init__(jid, password)
        
        park_id = cfg.get_jid_name(park_jid).replace("park_manager_", "")
        self.logger = create_kiosk_exit_logger(park_id)
        
        self.park_jid = park_jid
        self.tarifa_minuto = tarifa_minuto
        self.hora_fecho = hora_fecho
        self.multa_fixa = multa_fixa

        self.vehicle_waiting_payment = None
        self.current_vehicle_id = None
        self.value_to_pay = None
    
    async def setup(self):
        self.add_behaviour(RecvPaymentRequest())
        self.add_behaviour(RecvEntryTimeResponse())
        self.add_behaviour(RecvPaymentConfirmation())
    
    def calculate_payment(self, entry_time):
        now = datetime.now()
        real_diff_seconds = (now - entry_time).total_seconds()

        simulated_seconds = real_diff_seconds * cfg.get_time_factor()
        minutos_simulados = max(1, int(simulated_seconds // 60))

        valor = minutos_simulados * self.tarifa_minuto

        hora_fecho_obj = datetime.strptime(self.hora_fecho, "%H:%M").time()
        now_time = now.time()

        if now_time > hora_fecho_obj:
            hoje_fecho = now.replace(hour=hora_fecho_obj.hour, minute=hora_fecho_obj.minute, second=0, microsecond=0)
            excedente_real_seconds = (now - hoje_fecho).total_seconds()
            
            if excedente_real_seconds > 0:
                excedente_simulated_seconds = excedente_real_seconds * cfg.get_time_factor()
                excedente_minutos = max(1, int(excedente_simulated_seconds // 60))
                valor += self.multa_fixa + (excedente_minutos * self.tarifa_minuto)

        return round(valor, 2)