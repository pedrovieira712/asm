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
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "HORA_ENTRADA":
            return
        
        # body: {"id_veiculo": "ABC123", "hora_entrada": datetime_obj}
        dados = eval(msg.body) if isinstance(msg.body, str) else msg.body
        id_veiculo = dados.get("id_veiculo")
        hora_entrada = dados.get("hora_entrada")
        
        # Guarda a hora de entrada do veículo
        self.agent.horas_entrada[id_veiculo] = hora_entrada
        print(f"[Quiosque Saída] Hora de entrada registada para {id_veiculo}: {hora_entrada}")

# Behaviour para receber pedidos de saída e calcular o preço
class RecvExitRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "PEDIDO_PAGAMENTO":
            return
        
        id_veiculo = msg.body
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
            
            # Envia valor ao veículo
            msg_veiculo = Message(to=str(msg.sender))
            msg_veiculo.metadata["tipo"] = "VALOR_A_PAGAR"
            msg_veiculo.body = str(round(valor, 2))
            await self.send(msg_veiculo)
            
            print(f"[Quiosque Saída] Valor calculado para {id_veiculo}: €{valor:.2f} ({tempo_permanencia:.0f} min)")
        else:
            # Veículo não tem hora de entrada registada
            msg_veiculo = Message(to=str(msg.sender))
            msg_veiculo.metadata["tipo"] = "ERRO"
            msg_veiculo.body = "Hora de entrada não encontrada"
            await self.send(msg_veiculo)
            print(f"[Quiosque Saída] ❌ Hora de entrada não encontrada para {id_veiculo}")

# Behaviour para receber o pagamento e avisar ao Manager sobre isso
class RecvPayment(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        tipo_msg = msg.metadata.get("tipo")
        if tipo_msg != "PAGAMENTO":
            return
        
        # body: {"id_veiculo": "ABC123", "valor_pago": 10.5}
        dados = eval(msg.body) if isinstance(msg.body, str) else msg.body
        id_veiculo = dados.get("id_veiculo")
        valor_pago = dados.get("valor_pago")
        
        print(f"[Quiosque Saída] ✅ Pagamento recebido de {id_veiculo}: €{valor_pago}")
        
        # Notifica o Manager que o veículo pagou
        if hasattr(self.agent, 'manager_jid'):
            msg_manager = Message(to=self.agent.manager_jid)
            msg_manager.metadata["tipo"] = "CONFIRMACAO_PAGAMENTO"
            msg_manager.body = str({"id_veiculo": id_veiculo, "hora_pagamento": datetime.now(), "valor": valor_pago})
            await self.send(msg_manager)
            print(f"[Quiosque Saída] Pagamento de {id_veiculo} notificado ao Manager")
        
        # Confirma ao veículo
        msg_veiculo = Message(to=str(msg.sender))
        msg_veiculo.metadata["tipo"] = "PAGAMENTO_OK"
        msg_veiculo.body = "Pagamento confirmado"
        await self.send(msg_veiculo)



