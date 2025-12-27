from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio
from Config import Config as cfg

class ReceiveRedirectRequestsBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "redirect_park_request" and cfg.identify(msg.sender) == "vehicle":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            current_location = msg_body.get("current_location")

            vehicle_info = msg_body.get("vehicle_info", {})
            print(f"[CentralManager] Received redirect request from Vehicle {vehicle_id} at location {current_location}.")

            self.agent.add_redirect_request(vehicle_id, vehicle_info)

            self.agent.add_behaviour(
                SendLocationRequestBehaviour(vehicle_id, current_location)
            )

class SendLocationRequestBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id, current_location):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.current_location = current_location

    async def run(self):
        location_agent_jid = cfg.get_location_manager_jid()

        msg = Message(
            to=location_agent_jid,
            metadata={"performative": "closer_park_request"},
            body=jsonpickle.encode({
                "vehicle_id": self.vehicle_id,
                "current_location": self.current_location
            })
        )

        await self.send(msg)
        print(f"[CentralManager] Sent closer park request for vehicle {self.vehicle_id} to Location Manager.")

class ReceiveNextParkInfoBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "send_next_park_info" and cfg.identify(msg.sender) == "location_manager":
            msg_body = jsonpickle.decode(msg.body)

            closest_park = msg_body.get("closest_park")
            vehicle_id = msg_body.get("vehicle_id")

            print(f"[CentralManager] Received closest park info for vehicle {vehicle_id}: {closest_park}.")

            vehicle_info = self.agent.get_redirect_requests().get(vehicle_id)

            if vehicle_info is not None:
                self.agent.add_behaviour(
                    SendAvailabilityRequest(vehicle_id, closest_park, vehicle_info)
                )

class SendAvailabilityRequest(OneShotBehaviour):
    def __init__(self, vehicle_id, park_jid, vehicle_info):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.park_jid = park_jid
        self.vehicle_info = vehicle_info

    async def run(self):
        msg = Message(
            to=self.park_jid,
            metadata={"performative": "redirect_vehicle_request"},
            body=jsonpickle.encode({
                "vehicle_id": self.vehicle_id,
                "vehicle_info": self.vehicle_info,
            })
        )

        await self.send(msg)
        print(f"[CentralManager] Sent availability request for vehicle {self.vehicle_id} to park {self.park_jid}.")

class ReceiveAvailabilityResponseBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "redirect_vehicle_response" and cfg.identify(msg.sender) == "park_manager":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            is_available = msg_body.get("is_available")
            park_location = msg_body.get("park_location")

            print(f"[CentralManager] Received availability response for vehicle {vehicle_id} from park {park_location}.")

            if is_available:
                self.agent.add_behaviour(
                    SendRedirectResponseBehaviour(vehicle_id, park_location)
                )
                self.agent.remove_redirect_request(vehicle_id)

            else:
                self.agent.add_behaviour(
                    SendLocationRequestBehaviour(vehicle_id, park_location)
                )

class SendRedirectResponseBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id, park_location):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.park_location = park_location

    async def run(self):
        vehicle_jid = cfg.get_vehicle_jid(self.vehicle_id)

        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "redirect_park_response"},
            body=jsonpickle.encode({
                "next_location": self.park_location,
            })
        )

        await self.send(msg)
        print(f"[CentralManager] Sent redirect approval to vehicle {self.vehicle_id} for park at {self.park_location}.")



        

