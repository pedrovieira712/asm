from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle

class RecvRequestsLocation(CyclicBehaviour):
    pass

class SendLocationInfo(OneShotBehaviour):
    pass