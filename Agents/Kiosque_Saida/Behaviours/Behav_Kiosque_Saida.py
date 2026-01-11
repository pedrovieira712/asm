from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import jsonpickle
from datetime import datetime
from Config import Config as cfg


class RecvPaymentRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "payment_request" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")
            self.agent.logger.info(f"Payment request received from vehicle {vehicle_id}")
            
            self.agent.vehicle_waiting_payment = str(msg.sender)
            self.agent.current_vehicle_id = vehicle_id
            
            msg_park = Message(
                to=self.agent.park_jid,
                metadata={"performative": "request_entry_time"},
                body=jsonpickle.encode({"vehicle_id": self.agent.current_vehicle_id})
            )
            await self.send(msg_park)
            
class RecvEntryTimeResponse(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "entry_time_response" and cfg.identify(msg.sender) == "park_manager":
            msg_body = jsonpickle.decode(msg.body)
            entry_time = msg_body.get("entry_time")  
            vehicle_id = msg_body.get("vehicle_id")
            
            if vehicle_id != getattr(self.agent, "current_vehicle_id", None):
                return 
            
            
            value_to_pay = self.agent.calculate_payment(entry_time)
            self.agent.value_to_pay = value_to_pay
            
            self.agent.add_behaviour(
                SendPaymentInfo(self.agent.vehicle_waiting_payment, value_to_pay)
            )

class SendPaymentInfo(OneShotBehaviour):
    def __init__(self, vehicle_jid, value):
        super().__init__()
        self.vehicle_jid = vehicle_jid
        self.value = value

    async def run(self):
        msg = Message(
            to=self.vehicle_jid,
            metadata={"performative": "payment_amount"},
            body=jsonpickle.encode({"amount": self.value})
        )
        await self.send(msg)
        self.agent.logger.info(f"Sent payment amount {self.value}€ to vehicle {cfg.get_jid_name(self.vehicle_jid).replace('vehicle_', '').upper()}")
       
class RecvPaymentConfirmation(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "payment_done" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")
            self.agent.logger.success(f"Payment received from vehicle {vehicle_id}")
            
            
            self.agent.add_behaviour(
                NotifyManagerPaymentDone(self.agent.park_jid, vehicle_id)
            )

class NotifyManagerPaymentDone(OneShotBehaviour):
    def __init__(self, manager_jid, vehicle_id):
        super().__init__()
        self.manager_jid = manager_jid
        self.vehicle_id = vehicle_id

    async def run(self):
        msg = Message(
            to=self.manager_jid,
            metadata={"performative": "payment_confirmed"},
            body=jsonpickle.encode({"vehicle_id": self.vehicle_id})
        )
        await self.send(msg)
        self.agent.logger.info(f"Notified park manager of payment confirmation for vehicle {self.vehicle_id}")