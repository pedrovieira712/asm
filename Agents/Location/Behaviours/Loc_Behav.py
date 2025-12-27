from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Config import Config as cfg

class RecvRequestsLocation(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return
        
        if msg.metadata.get("performative") == "closer_park_request" and cfg.identify(msg.sender) == "central_manager":
            msg_body = jsonpickle.decode(msg.body)
            manager_jid = str(msg.sender)
            current_location = msg_body["current_location"]
            vehicle_id = msg_body["vehicle_id"]

            closest_park = self.agent.get_closest_park(current_location)

            print(f"[Location Manager] Closest park to vehicle {vehicle_id} at location {current_location} is {closest_park}.")
            

            if closest_park is not None:
                self.agent.add_behaviour(
                    SendLocationInfo(closest_park, vehicle_id, manager_jid)
                )

 
class SendLocationInfo(OneShotBehaviour):
    def __init__(self, closest_park, vehicle_id, manager_jid):
        super().__init__()
        self.closest_park = closest_park
        self.vehicle_id = vehicle_id
        self.manager_jid = manager_jid

    async def run(self):
        msg = Message(
            to=self.manager_jid,
            metadata={"performative": "send_next_park_info"},
            body=jsonpickle.encode({
                "closest_park": self.closest_park,
                "vehicle_id": self.vehicle_id
            })
        )

        await self.send(msg)
        print(f"[Location Manager] Sent closest park info of vehicle {self.vehicle_id} to Central Manager.")