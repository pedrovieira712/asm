# ManagerParque/Behaviours/Mp_Behav.py
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime


class VerificarEntradaKiosque(CyclicBehaviour):
    """
    Diagrama: Entrada Disponível / Entrada Não Disponível
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("tipo") != "ENTRADA_VERIFICAR":
            return

        dados_veiculo = eval(msg.body) if msg.body else {}
        manager = self.agent

        if manager.has_free_spot_for(dados_veiculo):
            # Pode entrar
            resposta = Message(to=str(msg.sender))
            resposta.metadata["tipo"] = "ENTRADA_RESPOSTA"
            resposta.body = "PODE_ENTRAR"
            await self.send(resposta)

            # Informar sensor que existe lugar livre (opcional)
            sensor = dados_veiculo.get("sensor")
            if sensor:
                sensor_msg = Message(to=sensor)
                sensor_msg.metadata["tipo"] = "LUGAR_LIVRE"
                await self.send(sensor_msg)

            # Reserva lugar
            manager.occupied_spots += 1

        else:
            # Não pode entrar
            resposta = Message(to=str(msg.sender))
            resposta.metadata["tipo"] = "ENTRADA_RESPOSTA"
            resposta.body = "NAO_PODE_ENTRAR"
            await self.send(resposta)


class ProcessarSaidaBarreira(CyclicBehaviour):
    """
    Diagramas: Saída para sair / Multa
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("tipo") != "PEDIDO_SAIR":
            return

        manager = self.agent
        id_veiculo = msg.body
        agora = datetime.now()

        pago, atrasado = manager.is_payment_valid(id_veiculo, agora)

        resposta = Message(to=str(msg.sender))
        resposta.metadata["tipo"] = "RESPOSTA_SAIDA"

        if not pago:
            resposta.body = "PAGAMENTO_PENDENTE"

        else:
            if atrasado:
                manager.add_fine(id_veiculo, "Excedeu tempo após pagamento")
                resposta.body = "ABRIR_BARREIRA_COM_MULTA"
            else:
                resposta.body = "ABRIR_BARREIRA"

            if manager.occupied_spots > 0:
                manager.occupied_spots -= 1

        await self.send(resposta)


class ResponderReencaminhamentoCentral(CyclicBehaviour):
    """
    Diagramas: Reencaminhamento 1 e 2
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("tipo") != "VERIFICAR_LUGAR":
            return

        dados_veiculo = eval(msg.body) if msg.body else {}
        manager = self.agent

        pode = manager.has_free_spot_for(dados_veiculo)

        resposta = Message(to=str(msg.sender))
        resposta.metadata["tipo"] = "RESPOSTA_VERIFICAR_LUGAR"
        resposta.body = "SIM" if pode else "NAO"
        await self.send(resposta)
