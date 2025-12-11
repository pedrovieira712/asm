from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle


class ReceberPedidoSaida(CyclicBehaviour): # Veiculo ->
    pass

class VerificarPagamento(OneShotBehaviour): # -> Manager
    pass

class ReceberConfirmacaoPagamento(CyclicBehaviour): # Manager ->
    pass

class EnviarConfirmacaoSaida(OneShotBehaviour): # -> Sensor
    pass