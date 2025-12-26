from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio

class RecvForwarding(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "REENCAMINHAMENTO":
            return
        
        # Recebe pedido de reencaminhamento
        dados_veiculo = eval(msg.body) if isinstance(msg.body, str) else msg.body
        
        print(f"[Central Manager] Pedido de reencaminhamento recebido")
        
        # Guarda pedido para processar
        self.agent.pedido_reencaminhamento = {
            "dados_veiculo": dados_veiculo,
            "veiculo_sender": str(msg.sender)
        }

class SendParkingSpotRequest(CyclicBehaviour):
    async def run(self):
        if not hasattr(self.agent, 'pedido_reencaminhamento') or not hasattr(self.agent, 'localizacao_pedida'):
            self.agent.localizacao_pedida = False
        
        if self.agent.pedido_reencaminhamento and not self.agent.localizacao_pedida:
            # Pede ao Location o parque mais próximo
            if hasattr(self.agent, 'location_jid'):
                msg_location = Message(to=self.agent.location_jid)
                msg_location.metadata["tipo"] = "PARQUE_PROXIMO"
                msg_location.body = "Preciso do parque mais próximo"
                await self.send(msg_location)
                
                self.agent.localizacao_pedida = True
                print(f"[Central Manager] Pedido de localização enviado")
        
        await asyncio.sleep(0.1)

class RecvNextParkingSpot(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "PARQUE":
            return
        
        # Recebe parque sugerido pela Localização
        parque_jid = msg.body
        self.agent.parque_sugerido = parque_jid
        
        print(f"[Central Manager] Parque sugerido: {parque_jid}")
        
        # Envia pedido ao Manager do Parque para verificar disponibilidade
        if hasattr(self.agent, 'pedido_reencaminhamento'):
            dados_veiculo = self.agent.pedido_reencaminhamento.get("dados_veiculo")
            
            msg_manager = Message(to=parque_jid)
            msg_manager.metadata["tipo"] = "VERIFICAR_LUGAR"
            msg_manager.body = str(dados_veiculo)
            await self.send(msg_manager)
            
            print(f"[Central Manager] Verificação de lugar enviada ao parque {parque_jid}")

class SendParkingSpotAproval(OneShotBehaviour):
    async def run(self):
        # Pode ser usado para enviar aprovações adicionais
        pass

class RecvParkingSpotAproval(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "RESPOSTA_VERIFICAR_LUGAR":
            return
        
        resposta = msg.body  # "SIM" ou "NAO"
        central = self.agent
        
        if not hasattr(central, 'pedido_reencaminhamento') or not central.pedido_reencaminhamento:
            return
        
        veiculo_sender = central.pedido_reencaminhamento.get("veiculo_sender")
        
        if resposta == "SIM":
            # Parque tem vaga - informa veículo
            msg_veiculo = Message(to=veiculo_sender)
            msg_veiculo.metadata["tipo"] = "PARQUE_ALTERNATIVO"
            msg_veiculo.body = f"Vai para o parque {central.parque_sugerido}"
            await self.send(msg_veiculo)
            
            print(f"[Central Manager] ✅ Veículo reencaminhado para {central.parque_sugerido}")
        
        else:
            # Parque não tem vaga - continua procurando
            print(f"[Central Manager] ❌ Parque {central.parque_sugerido} sem vagas - continua procurando...")
            # Pode pedir outro parque à Localização
        
        # Limpa pedido
        central.pedido_reencaminhamento = None
        central.localizacao_pedida = False

class SendUpdateParkingSpotInfo(OneShotBehaviour):
    async def run(self):
        # Pode ser usado para atualizar informações dos parques
        pass