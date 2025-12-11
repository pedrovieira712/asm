# ZonadeEspera/Behaviours/behaviours.py

from spade.behaviour import CyclicBehaviour
from spade.message import Message


class ReceberPedidosEspera(CyclicBehaviour):
    """
    Recebe veículos que devem ser colocados na fila de espera.
    Mensagem esperada:
        metadata["tipo"] = "ENTRAR_ESPERA"
        body = id do veículo
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("tipo") != "ENTRAR_ESPERA":
            return

        veiculo = msg.body
        zona = self.agent

        zona.fila.append(veiculo)
        zona.print(f"Veículo {veiculo} colocado na fila. Fila atual: {zona.fila}")

        # Responder ao ManagerParque (opcional)
        resposta = Message(to=str(msg.sender))
        resposta.metadata["tipo"] = "ENTRAR_ESPERA_CONFIRMADO"
        await self.send(resposta)


class FornecerVeiculoAoParque(CyclicBehaviour):
    """
    ManagerParque -> ZonaEspera:
        metadata["tipo"] = "PEDIR_VEICULO"

    ZonaEspera:
        se houver -> responde com "VEICULO"
        se não houver -> responde "SEM_VEICULO"
    """

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("tipo") != "PEDIR_VEICULO":
            return

        zona = self.agent

        resposta = Message(to=str(msg.sender))
        resposta.metadata["tipo"] = "RESPOSTA_PEDIR_VEICULO"

        if zona.fila:
            prox = zona.fila.pop(0)
            resposta.body = prox
            zona.print(f"Enviado veículo {prox} ao parque. Fila: {zona.fila}")
        else:
            resposta.body = "SEM_VEICULO"

        await self.send(resposta)
