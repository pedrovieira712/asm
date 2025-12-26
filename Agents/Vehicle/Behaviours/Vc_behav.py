from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio

class SendFowardingRequestBehaviour(OneShotBehaviour):
    async def run(self):
        # Aguarda até ter central_manager_jid configurado
        while not hasattr(self.agent, 'central_manager_jid'):
            await asyncio.sleep(0.1)
        
        # Envia pedido de reencaminhamento ao Manager Central
        msg = Message(to=self.agent.central_manager_jid)
        msg.metadata["tipo"] = "REENCAMINHAMENTO"
        
        # Dados do veículo
        dados_veiculo = {
            "id_veiculo": str(self.agent.jid),
            "vehicle_type": getattr(self.agent, 'vehicle_type', 'carro'),
            "user_type": getattr(self.agent, 'user_type', 'normal'),
            "plate": getattr(self.agent, 'plate', 'ABC-123')
        }
        msg.body = str(dados_veiculo)
        await self.send(msg)
        
        print(f"[Veículo {self.agent.jid}] Pedido de reencaminhamento enviado ao Manager Central")

class ReceiveFowardingResponseBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        
        if tipo_msg == "PARQUE_ALTERNATIVO":
            # Recebe sugestão de parque alternativo
            parque_info = msg.body
            print(f"[Veículo {self.agent.jid}] Parque alternativo recebido: {parque_info}")
            
            # Guarda informação do parque alternativo
            self.agent.parque_sugerido = parque_info
        
        elif tipo_msg == "ENTRADA_OK":
            # Autorizado a entrar
            print(f"[Veículo {self.agent.jid}] ✅ Autorizado a entrar no parque")
        
        elif tipo_msg == "NAO_PODE_ENTRAR":
            # Não pode entrar
            print(f"[Veículo {self.agent.jid}] ❌ Não pode entrar - precisa aguardar ou ir para outro parque")