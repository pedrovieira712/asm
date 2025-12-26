from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio

# Receber pedido de saída do veículo
class ReceberPedidoSaida(CyclicBehaviour): # Veiculo ->
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="request"
        if msg.metadata.get("performative") != "request":
            return
        
        # Deserializar com jsonpickle
        id_veiculo = jsonpickle.decode(msg.body)
        print(f"[Barreira Saída] Recebido pedido de saída do veículo: {id_veiculo}")
        
        # Guarda informações do pedido
        self.agent.pedido_veiculo = id_veiculo
        self.agent.veiculo_sender = str(msg.sender)

#Envia pedido de verificação de pagamento ao Manager
class VerificarPagamento(CyclicBehaviour): # -> Manager
    async def run(self):
        # Só processa se houver pedido E ainda não foi enviado
        if hasattr(self.agent, 'pedido_veiculo') and not hasattr(self.agent, 'pedido_enviado'):
            id_veiculo = self.agent.pedido_veiculo
            
            # Envia pedido ao Manager com performative="request"
            if hasattr(self.agent, 'manager_jid'):
                msg_manager = Message(
                    to=self.agent.manager_jid,
                    metadata={"performative": "request"},
                    body=jsonpickle.encode(id_veiculo)
                )
                await self.send(msg_manager)
                print(f"[Barreira Saída] Enviado pedido de verificação ao Manager para: {id_veiculo}")
                
                # Marca como enviado para não enviar novamente
                self.agent.pedido_enviado = True
        
        await asyncio.sleep(0.1)

# Receber confirmação de pagamento do Manager
class ReceberConfirmacaoPagamento(CyclicBehaviour): # Manager ->
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="confirm" ou "inform"
        if msg.metadata.get("performative") not in ["confirm", "inform"]:
            return
        
        # Deserializar resposta
        resposta_manager = jsonpickle.decode(msg.body)
        print(f"[Barreira Saída] Resposta do Manager: {resposta_manager}")
        
        # Guarda a resposta do Manager
        self.agent.resposta_pagamento = resposta_manager
        
        # Responde ao veículo com performative="inform"
        if hasattr(self.agent, 'veiculo_sender'):
            msg_veiculo = Message(
                to=self.agent.veiculo_sender,
                metadata={"performative": "inform"},
                body=jsonpickle.encode(resposta_manager)
            )
            await self.send(msg_veiculo)
            
            if resposta_manager == "PAGAMENTO_PENDENTE":
                print(f"[Barreira Saída] Barreira bloqueada - Pagamento pendente")
            elif resposta_manager == "ABRIR_BARREIRA_COM_MULTA":
                print(f"[Barreira Saída] Barreira aberta COM MULTA")
            else:
                print(f"[Barreira Saída] Barreira aberta")

# Enviar confirmação de saída ao Sensor
class EnviarConfirmacaoSaida(CyclicBehaviour): # -> Sensor
    async def run(self):
        # Só processa se tiver resposta E ainda não notificou
        if hasattr(self.agent, 'resposta_pagamento') and not hasattr(self.agent, 'sensor_notificado'):
            resposta = self.agent.resposta_pagamento
            
            # Só notifica sensor se a barreira abriu
            if resposta in ["ABRIR_BARREIRA", "ABRIR_BARREIRA_COM_MULTA"]:
                if hasattr(self.agent, 'sensor_jid'):
                    msg_sensor = Message(
                        to=self.agent.sensor_jid,
                        metadata={"performative": "inform"},
                        body=jsonpickle.encode("SENSOR_LIVRE")
                    )
                    await self.send(msg_sensor)
                    print(f"[Barreira Saída] Sensor notificado - Saída livre")
                
                # Marca como notificado
                self.agent.sensor_notificado = True
                
                # Limpa as flags para o próximo veículo
                if hasattr(self.agent, 'pedido_veiculo'):
                    delattr(self.agent, 'pedido_veiculo')
                if hasattr(self.agent, 'pedido_enviado'):
                    delattr(self.agent, 'pedido_enviado')
                if hasattr(self.agent, 'resposta_pagamento'):
                    delattr(self.agent, 'resposta_pagamento')
                if hasattr(self.agent, 'veiculo_sender'):
                    delattr(self.agent, 'veiculo_sender')
                if hasattr(self.agent, 'sensor_notificado'):
                    delattr(self.agent, 'sensor_notificado')
                
                print(f"[Barreira Saída] Pronta para próximo veículo")
        
        await asyncio.sleep(0.1)