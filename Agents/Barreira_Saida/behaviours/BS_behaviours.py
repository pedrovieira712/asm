from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Config import Config as cfg

class ReceiveExitRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "exit_request" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")

            self.agent.add_behaviour(
                SendRequestPaymentCheck(vehicle_id)
            )

            self.agent.logger.info(f"Exit request received for vehicle {vehicle_id}")


class SendRequestPaymentCheck(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        msg = Message(
            to=self.agent.park_jid,
            metadata={"performative": "send_request_payment_check"},
            body=jsonpickle.encode({"vehicle_id": self.vehicle_id})
        )

        await self.send(msg)
        

class ReceivePaymentConfirmation(CyclicBehaviour): 
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") in ["confirm_payment"] and cfg.identify(msg.sender) == "park_manager":
            msg_body = jsonpickle.decode(msg.body)
            sensor_jid = msg_body["sensor_jid"]
            vehicle_id = msg_body["vehicle_id"]

            if msg.metadata.get("performative") == "confirm_payment":
                self.agent.logger.success(f"Barrier opened for vehicle {vehicle_id}")
                self.agent.add_behaviour(
                    SendExitConfirmation(sensor_jid)
                )
            
            
class SendExitConfirmation(OneShotBehaviour): 
    def __init__(self, sensor_jid):
        super().__init__()
        self.sensor_jid = sensor_jid

    async def run(self):
        msg_sensor = Message(
            to=self.sensor_jid,
            metadata={"performative": "exit_confirmed"},
        )

        await self.send(msg_sensor)

