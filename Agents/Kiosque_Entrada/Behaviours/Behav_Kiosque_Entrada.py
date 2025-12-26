from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from datetime import datetime
import asyncio

# Behaviour para receber pedidos de entrada de veículos
class RecvEntryRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="request"
        if msg.metadata.get("performative") != "request":
            return
        
        # Deserializar com jsonpickle
        dados_veiculo = jsonpickle.decode(msg.body)
        id_veiculo = dados_veiculo.get("id_veiculo")
        
        print(f"[Quiosque Entrada] Pedido de entrada do veículo: {id_veiculo}")
        
        # Guarda pedido para processar
        self.agent.pedido_entrada = {
            "dados_veiculo": dados_veiculo,
            "veiculo_sender": str(msg.sender)
        }

# Behaviour para verificar disponibilidade com o ManagerParque pergunta se há vaga
class CheckAvailability(CyclicBehaviour):
    async def run(self):
        if not hasattr(self.agent, 'pedido_entrada') or not hasattr(self.agent, 'verificacao_enviada'):
            self.agent.verificacao_enviada = False
        
        if self.agent.pedido_entrada and not self.agent.verificacao_enviada:
            dados_veiculo = self.agent.pedido_entrada.get("dados_veiculo")
            
            # Envia pedido de verificação ao Manager com performative="request"
            if hasattr(self.agent, 'manager_jid'):
                msg_manager = Message(
                    to=self.agent.manager_jid,
                    metadata={"performative": "request"},
                    body=jsonpickle.encode(dados_veiculo)
                )
                await self.send(msg_manager)
                
                self.agent.verificacao_enviada = True
                print(f"[Quiosque Entrada] Verificação enviada ao Manager")
        
        await asyncio.sleep(0.1)

# Behaviour para validar passe anual
class ValidateAnnualPass(CyclicBehaviour):
    async def run(self):
        # Pode ser expandido para validar passes anuais
        await asyncio.sleep(0.5)

# Behaviour para registar a entrada do veículo, guarda hora de entrada, comunica com ManagerParque e Barreira de Entrada
class RegisterEntry(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="confirm" ou "inform"
        if msg.metadata.get("performative") not in ["confirm", "inform"]:
            return
        
        # Deserializar resposta
        resposta = jsonpickle.decode(msg.body)  # "PODE_ENTRAR" ou "NAO_PODE_ENTRAR"
        quiosque = self.agent
        
        if not hasattr(quiosque, 'pedido_entrada') or not quiosque.pedido_entrada:
            return
        
        dados_veiculo = quiosque.pedido_entrada.get("dados_veiculo")
        veiculo_sender = quiosque.pedido_entrada.get("veiculo_sender")
        id_veiculo = dados_veiculo.get("id_veiculo")
        
        if resposta == "PODE_ENTRAR":
            print(f"[Quiosque Entrada] ✅ Veículo {id_veiculo} pode entrar")
            
            # Registar hora de entrada
            hora_entrada = datetime.now()
            
            # Envia hora de entrada ao Quiosque de Saída com performative="inform"
            if hasattr(quiosque, 'quiosque_saida_jid'):
                entrada_data = {"id_veiculo": id_veiculo, "hora_entrada": hora_entrada.isoformat()}
                msg_saida = Message(
                    to=quiosque.quiosque_saida_jid,
                    metadata={"performative": "inform"},
                    body=jsonpickle.encode(entrada_data)
                )
                await self.send(msg_saida)
            
            # Confirma ao veículo com performative="confirm"
            msg_veiculo = Message(
                to=veiculo_sender,
                metadata={"performative": "confirm"},
                body=jsonpickle.encode("ENTRADA_APROVADA")
            )
            await self.send(msg_veiculo)
            
            print(f"[Quiosque Entrada] Veículo {id_veiculo} autorizado a entrar")
        
        else:  # NAO_PODE_ENTRAR
            print(f"[Quiosque Entrada] ❌ Veículo {id_veiculo} não pode entrar")
            # Ativa comportamento de sugerir alternativas
            quiosque.precisa_alternativas = True
        
        # Limpa pedido
        quiosque.pedido_entrada = None
        quiosque.verificacao_enviada = False

# Behaviour para sugerir alternativas se o parque estiver cheio, comunica com CentralManager, recebe lista de parques alternativos e envia sugestões ao veículo
class SuggestAlternatives(CyclicBehaviour):
    async def run(self):
        if not hasattr(self.agent, 'precisa_alternativas') or not self.agent.precisa_alternativas:
            await asyncio.sleep(0.5)
            return
        
        # Envia pedido de reencaminhamento ao CentralManager com performative="request"
        if hasattr(self.agent, 'central_manager_jid'):
            msg_central = Message(
                to=self.agent.central_manager_jid,
                metadata={"performative": "request"},
                body=jsonpickle.encode("REENCAMINHAMENTO")
            )
            await self.send(msg_central)
            
            print(f"[Quiosque Entrada] Pedido de alternativas enviado ao Central Manager")
            self.agent.precisa_alternativas = False
        
        await asyncio.sleep(0.5)

# Behaviour para receber e armazenar informações do parque (como ocupação, horários)
class RecvParkInfo(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg == "PARK_INFO":
            info = msg.body
            print(f"[Quiosque Entrada] Informação do parque recebida: {info}")

# Behaviour para enviar confirmação de entrada ao veículo
class SendEntryConfirmation(OneShotBehaviour):
    async def run(self):
        # Pode ser usado para confirmações adicionais
        pass

# Behaviour para processar compra de passe anual - vai dar para comprar no """"app"""""
class ProcessAnnualPassPurchase(CyclicBehaviour):
    async def run(self):
        # Pode ser expandido para processar compra de passes
        await asyncio.sleep(1)
