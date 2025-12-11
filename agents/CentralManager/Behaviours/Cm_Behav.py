from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle

class RecvForwarding(CyclicBehaviour):
    pass

class SendParkingSpotRequest(OneShotBehaviour):
    pass

class RecvNextParkingSpot(OneShotBehaviour):
    pass

class SendParkingSpotAproval(OneShotBehaviour):
    pass

class RecvParkingSpotAproval(OneShotBehaviour):
    pass

class SendUpdateParkingSpotInfo(OneShotBehaviour):
    pass