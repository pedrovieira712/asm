# ZonadeEspera/zonadeespera.py

from spade.agent import Agent
from ZonadeEspera.Behaviours.behaviours import *


class ZonadeEspera(Agent):
    """
    Agente de Zona de Espera - gere a fila de veículos em espera.
    """

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.fila = []  # Fila de veículos em espera

    def print(self, txt):
        print(f"[ZONA_ESPERA] {txt}")

    async def setup(self):
        self.print("Zona de Espera a iniciar...")
        
        # Adicionar behaviour para receber veículos na fila de espera
        self.add_behaviour(ReceberPedidosEspera())
        
        # Adicionar behaviour para fornecer veículos ao parque
        self.add_behaviour(FornecerVeiculoAoParque())
        
        self.print("Behaviours adicionados com sucesso!")
