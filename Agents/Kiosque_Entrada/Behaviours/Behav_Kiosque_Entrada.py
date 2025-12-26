from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from datetime import datetime

# Behaviour para receber pedidos de entrada de veículos
class RecvEntryRequest(CyclicBehaviour):
    pass

# Behaviour para verificar disponibilidade com o ManagerParque pergunta se há vaga
class CheckAvailability(CyclicBehaviour):
    pass

# Behaviour para validar passe anual
class ValidateAnnualPass(CyclicBehaviour):
    pass

# Behaviour para registar a entrada do veículo, guarda hora de entrada, comunica com ManagerParque e Barreira de Entrada
class RegisterEntry(CyclicBehaviour):
    pass

# Behaviour para sugerir alternativas se o parque estiver cheio, comunica com CentralManager, recebe lista de parques alternativos e envia sugestões ao veículo
class SuggestAlternatives(CyclicBehaviour):
    pass

# Behaviour para receber e armazenar informações do parque (como ocupação, horários)
class RecvParkInfo(CyclicBehaviour):
    pass

# Behaviour para enviar confirmação de entrada ao veículo
class SendEntryConfirmation(OneShotBehaviour):
    pass

# Behaviour para processar compra de passe anual - vai dar para comprar no """"app"""""
class ProcessAnnualPassPurchase(CyclicBehaviour):
    pass
