from spade.agent import Agent
from Barreira_Saida.behaviours.BS_behaviours import *


class BarreiraSaida(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        
        
        
    async def setup(self):
        print(f"Barreira de Saída {self.jid} iniciada.")
        
        receber_pedido_saida = ReceberPedidoSaida()
        self.add_behaviour(receber_pedido_saida)
        
        verificar_pagamento = VerificarPagamento()
        self.add_behaviour(verificar_pagamento)
        
        receber_confirmacao_pagamento = ReceberConfirmacaoPagamento()
        self.add_behaviour(receber_confirmacao_pagamento)
        
        enviar_confirmacao_saida = EnviarConfirmacaoSaida()
        self.add_behaviour(enviar_confirmacao_saida)
        
        