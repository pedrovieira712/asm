from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio

class RecvRequestsLocation(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "PARQUE_PROXIMO":
            return
        
        print(f"[Location] Pedido de parque próximo recebido")
        
        # Guarda pedido
        self.agent.pedido_localizacao = str(msg.sender)

class SendLocationInfo(CyclicBehaviour):
    async def run(self):
        if not hasattr(self.agent, 'pedido_localizacao') or not self.agent.pedido_localizacao:
            await asyncio.sleep(0.5)
            return
        
        location = self.agent
        
        # Obtém parque mais próximo (simplificado - pega o primeiro da lista)
        if hasattr(location, 'park_locations') and location.park_locations:
            parque_proximo = list(location.park_locations.keys())[0]
            
            # Envia ao Central Manager
            msg = Message(to=location.pedido_localizacao)
            msg.metadata["tipo"] = "PARQUE"
            msg.body = parque_proximo
            await self.send(msg)
            
            print(f"[Location] Parque próximo enviado: {parque_proximo}")
        
        # Limpa pedido
        location.pedido_localizacao = None
        await asyncio.sleep(0.1)