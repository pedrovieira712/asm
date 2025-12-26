from spade.agent import Agent
import asyncio
from datetime import datetime
from Kiosque_Entrada.Behaviours.Behav_Kiosque_Entrada import *

class Kiosque_Entrada(Agent):
    """
    Quiosque de Entrada - Ponto inicial de interação com o parque
    Responsável por:
    - Receber pedidos de entrada
    - Verificar disponibilidade
    - Validar passes anuais
    - Registar hora de entrada
    - Comunicar com Manager do Parque e Barreira de Entrada
    """
    
    def __init__(self, jid, password, park_id):
        super().__init__(jid, password)
        self.park_id = park_id
        self.vehicles_waiting = {}  # Veículos à espera de entrada
        self.annual_passes = {}  # Base de dados de passes anuais {matricula: {validade, tipo}}
        
    async def setup(self):
        print(f"[KIOSQUE_ENTRADA - Parque {self.park_id}] Iniciado")
        
        # Receber pedidos de entrada de veículos
        recv_entry_request_behav = RecvEntryRequest()
        self.add_behaviour(recv_entry_request_behav)
        
        # Verificar disponibilidade com o ManagerParque
        check_availability_behav = CheckAvailability()
        self.add_behaviour(check_availability_behav)

        # Validar passe anual
        validate_annual_pass_behav = ValidateAnnualPass()
        self.add_behaviour(validate_annual_pass_behav)

        # Registar entrada e comunicar com barreira
        register_entry_behav = RegisterEntry()
        self.add_behaviour(register_entry_behav)

        # Oferecer alternativas se parque cheio
        suggest_alternatives_behav = SuggestAlternatives()
        self.add_behaviour(suggest_alternatives_behav)

        # Receber informações do parque (ocupação, tarifas, horários)
        recv_park_info_behav = RecvParkInfo()
        self.add_behaviour(recv_park_info_behav)
