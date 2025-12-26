from spade.agent import Agent
import asyncio
from datetime import datetime
from Behaviours.Behav_Kiosque_Saida import *

class Kiosque_saida(Agent):
    tarifa_minuto = 0.05
    hora_fecho = "22:00" # Exemplo
    multa_fixa = 5.00
    def __init__(self, jid,password):
        super().__init__(jid, password)
        self.horas_entrada = {}
    async def setup(self):
        print("[KIOSQUE_SAIDA] Iniciado")
        RecvEntryHourClient_behav = RecvEntryHourClient()
        self.add_behaviour(RecvEntryHourClient_behav)

        recvExitRequest_behav = RecvExitRequest()
        self.add_behaviour(recvExitRequest_behav)

        RecvPayment_behav = RecvPayment()
        self.add_behaviour(RecvPayment_behav)