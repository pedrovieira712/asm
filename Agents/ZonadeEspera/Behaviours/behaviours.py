from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Config import Config as cfg

class VehicleWaitingRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "wait_entry" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")

            print(f"[Waiting Zone] Vehicle {vehicle_id} is requesting to enter the waiting zone at park {self.agent.park_jid}.")

            if vehicle_id:
                self.agent.add_waiting_vehicle(str(msg.sender))

class VehicleWaitingRequestExit(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "wait_exit" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")

            print(f"[Waiting Zone] Vehicle {vehicle_id} is requesting to exit the waiting zone at park {self.agent.park_jid}.")

            if vehicle_id:
                self.agent.remove_waiting_vehicle(str(msg.sender))





            



