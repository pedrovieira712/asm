from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime, timedelta
from Config import Config as cfg
import asyncio
import jsonpickle


class RecvExitConfirmed(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("performative") == "exit_confirmed" and cfg.identify(msg.sender) == "barrier_exit":
            self.agent.is_free = True
            self.agent.vehicle_id = None
            print(f"[Sensor {self.agent.id_lugar}] Spot freed (exit confirmed) in park {self.agent.park_jid}.")

class RecvMarkSpot(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if msg.metadata.get("performative") == "mark_spot" and cfg.identify(msg.sender) == "park_manager":
            msg_body = jsonpickle.decode(msg.body)
            vehicle_id = msg_body.get("vehicle_id")

            self.agent.is_free = False
            self.agent.vehicle_id = vehicle_id
            print(f"[Sensor {self.agent.id_lugar}] Spot occupied by vehicle {vehicle_id} in park {self.agent.park_jid}.")