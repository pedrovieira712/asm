from spade.agent import Agent
import asyncio
from datetime import datetime
from .Behaviours.Behav_Kiosque_Saida import *

class Kiosque_saida(Agent):
    def __init__(self, jid, password, park_jid, tarifa_minuto, hora_fecho, multa_fixa):
        super().__init__(jid, password)
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
    
    def calculate_payment(self, entry_time_input):
        if isinstance(entry_time_input, str):
            entry_time = datetime.strptime(entry_time_input, "%Y-%m-%d %H:%M:%S")
        elif isinstance(entry_time_input, datetime):
            entry_time = entry_time_input
        else:
            raise ValueError("entry_time_input deve ser string ou datetime.datetime")

        now = datetime.now()

        diff = now - entry_time
        minutos = int(diff.total_seconds() // 60)

        valor = minutos * self.tarifa_minuto

        hora_fecho_obj = datetime.strptime(self.hora_fecho, "%H:%M").time()
        now_time = now.time()

        if now_time > hora_fecho_obj:
            hoje_fecho = now.replace(hour=hora_fecho_obj.hour, minute=hora_fecho_obj.minute, second=0, microsecond=0)
            excedente_segundos = (now - hoje_fecho).total_seconds()
            excedente_minutos = int(excedente_segundos // 60)

            valor += self.multa_fixa + (excedente_minutos * self.tarifa_minuto)

        return round(valor, 2)