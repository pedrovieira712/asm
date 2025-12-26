from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import jsonpickle
from datetime import datetime

# Behaviour para receber as horas de entradas dos clientes
class RecvEntryHourClient(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="inform"
        if msg.metadata.get("performative") != "inform":
            return
        
        # Deserializar com jsonpickle
        dados = jsonpickle.decode(msg.body)
        id_veiculo = dados.get("id_veiculo")
        hora_entrada_str = dados.get("hora_entrada")
        
        # Converter string ISO para datetime
        hora_entrada = datetime.fromisoformat(hora_entrada_str) if isinstance(hora_entrada_str, str) else hora_entrada_str
        
        # Guarda a hora de entrada do veículo
        self.agent.horas_entrada[id_veiculo] = hora_entrada
        print(f"[Quiosque Saída] Hora de entrada registada para {id_veiculo}: {hora_entrada}")

# Behaviour para receber pedidos de saída e calcular o preço
class RecvExitRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="request"
        if msg.metadata.get("performative") != "request":
            return
        
        # Deserializar
        id_veiculo = jsonpickle.decode(msg.body)
        quiosque = self.agent
        
        print(f"[Quiosque Saída] Pedido de pagamento do veículo: {id_veiculo}")
        
        # Calcula o valor a pagar
        if id_veiculo in quiosque.horas_entrada:
            hora_entrada = quiosque.horas_entrada[id_veiculo]
            hora_saida = datetime.now()
            
            # Calcula tempo de permanência em minutos
            tempo_permanencia = (hora_saida - hora_entrada).total_seconds() / 60
            valor = tempo_permanencia * quiosque.tarifa_minuto
            
            # Verifica se passou da hora de fecho e adiciona multa
            if hora_saida.time() > datetime.strptime(quiosque.hora_fecho, "%H:%M").time():
                valor += quiosque.multa_fixa
                print(f"[Quiosque Saída] ⚠️ Passou da hora de fecho! Multa adicionada.")
            
            # Envia valor ao veículo com performative="inform"
            msg_veiculo = Message(
                to=str(msg.sender),
                metadata={"performative": "inform"},
                body=jsonpickle.encode({"valor": round(valor, 2), "tempo_minutos": tempo_permanencia})
            )
            await self.send(msg_veiculo)
            
            print(f"[Quiosque Saída] Valor calculado para {id_veiculo}: €{valor:.2f} ({tempo_permanencia:.0f} min)")
        else:
            # Veículo não tem hora de entrada registada - envia erro
            msg_veiculo = Message(
                to=str(msg.sender),
                metadata={"performative": "inform"},
                body=jsonpickle.encode({"erro": "Hora de entrada não encontrada"})
            )
            await self.send(msg_veiculo)
            print(f"[Quiosque Saída] ❌ Hora de entrada não encontrada para {id_veiculo}")

# Behaviour para receber o pagamento e avisar ao Manager sobre isso
class RecvPayment(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        # Formato ACL: performative="inform"
        if msg.metadata.get("performative") != "inform":
            return
        
        # Deserializar dados do pagamento
        dados = jsonpickle.decode(msg.body)
        id_veiculo = dados.get("id_veiculo") or dados.get("matricula")
        valor_pago = dados.get("valor_pago")
        
        print(f"[Quiosque Saída] ✅ Pagamento recebido de {id_veiculo}: €{valor_pago}")
        
        # Notifica o Manager que o veículo pagou com performative="inform"
        if hasattr(self.agent, 'manager_jid'):
            pagamento_data = {
                "id_veiculo": id_veiculo, 
                "hora_pagamento": datetime.now().isoformat(), 
                "valor": valor_pago
            }
            msg_manager = Message(
                to=self.agent.manager_jid,
                metadata={"performative": "inform"},
                body=jsonpickle.encode(pagamento_data)
            )
            await self.send(msg_manager)
            print(f"[Quiosque Saída] Pagamento de {id_veiculo} notificado ao Manager")
        
        # Confirma ao veículo com performative="confirm"
        msg_veiculo = Message(
            to=str(msg.sender),
            metadata={"performative": "confirm"},
            body=jsonpickle.encode("PAGAMENTO_CONFIRMADO")
        )
        await self.send(msg_veiculo)



