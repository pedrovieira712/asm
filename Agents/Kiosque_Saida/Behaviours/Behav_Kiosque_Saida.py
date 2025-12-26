from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import jsonpickle

# Behaviour para receber as horas de entradas dos clientes
class RecvEntryHourClient(CyclicBehaviour):
    pass

# Behaviour para receber pedidos de saída e calcular o preço
class RecvExitRequest(CyclicBehaviour):
    pass

# Behaviour para receber o pagamento e avisar ao Manager sobre isso
class RecvPayment(CyclicBehaviour):
    pass



