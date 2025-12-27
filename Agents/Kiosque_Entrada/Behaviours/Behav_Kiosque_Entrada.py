from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from datetime import datetime
from Config import Config as cfg

class RecvEntryRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "entry_request" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")
            vehicle_info = msg_body.get("vehicle_info")
            
            print(f"[Entry Kiosk] Entry request from vehicle: {vehicle_id} at park {self.agent.park_jid}.")

            self.agent.mark_vehicle_waiting(vehicle_id)
            self.agent.register_vehicle(vehicle_id, str(msg.sender))
            
            self.agent.add_behaviour(
                SendEntryRequest(vehicle_info, vehicle_id)
            )


class SendEntryRequest(OneShotBehaviour):
    def __init__(self, vehicle_info, vehicle_id):
        super().__init__()
        self.vehicle_info = vehicle_info
        self.vehicle_id = vehicle_id

    async def run(self):
        msg = Message(
            to=self.agent.park_jid, 
            metadata={"performative": "entry_request"},
            body=jsonpickle.encode({
                "vehicle_info": self.vehicle_info,
                "vehicle_id": self.vehicle_id
            })
        )
        await self.send(msg)
        print(f"[Entry Kiosk] Entry request sent to park {self.agent.park_jid} from vehicle {self.vehicle_id}.")

class RecvEntryResponse(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "entry_response" and cfg.identify(msg.sender) == "park_manager":
            msg_body = jsonpickle.decode(msg.body) 
            state = msg_body.get("state")
            vehicle_id = msg_body.get("vehicle_id")

            if self.agent.is_vehicle_waiting(vehicle_id):
                self.agent.unmark_vehicle_waiting(vehicle_id)
                
                if state:
                    print(f"[Entry Kiosk] Vehicle {vehicle_id} authorized to enter in park {self.agent.park_jid}.")
                    self.agent.add_behaviour(SendEntryAuthorization(vehicle_id))

                else:
                    print(f"[Entry Kiosk] Vehicle {vehicle_id} not authorized to enter in park {self.agent.park_jid}.")
                    self.agent.add_behaviour(SendEntryDenial(vehicle_id))

class SendEntryAuthorization(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        vehicle_jid = self.agent.get_vehicle_jid(self.vehicle_id)
        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "entry_authorized"},
            body=jsonpickle.encode({"message": "Entry authorized"})
        )
        await self.send(msg)
        self.agent.unregister_vehicle(self.vehicle_id)
        print(f"[Entry Kiosk] Entry authorization sent to vehicle {self.vehicle_id} in park {self.agent.park_jid}.")


class SendEntryDenial(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        vehicle_jid = self.agent.get_vehicle_jid(self.vehicle_id)
        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "entry_denied"},
            body=jsonpickle.encode({"message": "Entry denied"})
        )
        await self.send(msg)
        self.agent.unregister_vehicle(self.vehicle_id)
        print(f"[Entry Kiosk] Entry denial sent to vehicle {self.vehicle_id} in park {self.agent.park_jid}.")

