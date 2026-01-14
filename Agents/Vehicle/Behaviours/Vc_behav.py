from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
import asyncio
from Config import Config as cfg

class SendEntryRequestBehaviour(OneShotBehaviour):
    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        kiosk_entry_jid = cfg.get_kiosk_entry_jid(park_manager_jid)

        if not self.agent.is_currently_parked():
            msg = Message(
                to=kiosk_entry_jid,
                metadata={"performative": "entry_request"},
                body=jsonpickle.encode({
                    "vehicle_id": self.agent.get_plate(),
                    "vehicle_info": {
                        "vehicle_type": self.agent.get_vehicle_type(),
                        "user_type": self.agent.get_user_type(),
                        "vehicle_height": self.agent.get_vehicle_height(),
                    }
                })
            )

            await self.send(msg)
            self.agent.logger.info(f"Entry request sent to kiosk entry")

class RecvEntryDecision(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "entry_authorized" and cfg.identify(msg.sender) == "kiosk_entry":
            body = jsonpickle.decode(msg.body)
            self.agent.logger.success("Entry authorized")
            if self.agent.is_waiting_at_park():
                self.agent.add_behaviour(SendExitWaitingZoneRequest())
            else:
                self.agent.reset_entry_retries()
                self.agent.set_parked(True)
                await asyncio.sleep(5)
                if not self.agent.is_skipping_payment_process():
                    self.agent.add_behaviour(SendPaymentRequest())
                else:
                    self.agent.set_payment_skipping(False)
                    self.agent.add_behaviour(SendExitRequest())

        elif performative == "entry_denied" and cfg.identify(msg.sender) == "kiosk_entry":
            body = jsonpickle.decode(msg.body)
            self.agent.logger.warning("Entry denied")

            if self.agent.prefers_redirect:
                self.agent.add_behaviour(SendRedirectRequest())
            else:
                self.agent.add_behaviour(WaitAtParkBehaviour())

            
class WaitAtParkBehaviour(OneShotBehaviour):
    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        wait_zone_jid = cfg.get_wait_zone_jid(park_manager_jid)

        msg = Message(
            to=wait_zone_jid,
            metadata={"performative": "wait_entry"},
            body=jsonpickle.encode({
                "vehicle_id": self.agent.get_plate(),
            })
        )

        await self.send(msg)
        self.agent.set_waiting(True)
        self.agent.increment_entry_retries()
        self.agent.logger.warning("Waiting at park, added to wait zone")

class SendExitWaitingZoneRequest(OneShotBehaviour):
    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        wait_zone_jid = cfg.get_wait_zone_jid(park_manager_jid)

        msg = Message(
            to=wait_zone_jid,
            metadata={"performative": "wait_exit"},
            body=jsonpickle.encode({
                "vehicle_id": self.agent.get_plate(),
            })
        )

        await self.send(msg)
        self.agent.logger.info("Exiting wait zone")

class SendRedirectRequest(OneShotBehaviour):
    async def run(self):
        central_manager_jid = cfg.get_central_manager_jid()

        msg = Message(
            to=central_manager_jid,
            metadata={"performative": "redirect_park_request"},
            body=jsonpickle.encode({
                "vehicle_id": self.agent.get_plate(),
                "current_location": self.agent.get_location(),
                 "vehicle_info": {
                    "vehicle_type": self.agent.get_vehicle_type(),
                    "user_type": self.agent.get_user_type(),
                    "vehicle_height": self.agent.get_vehicle_height(),
                }
            })
        )

        await self.send(msg)
        self.agent.logger.warning("Redirect request sent to central manager")


class RecvRedirectResponse(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "redirect_park_response" and cfg.identify(msg.sender) == "central_manager"):
            msg_body = jsonpickle.decode(msg.body)

            next_location = msg_body.get("next_location")

            self.agent.logger.success(f"Redirected to park at location {next_location}")

            self.agent.set_location(next_location)
            self.agent.add_behaviour(SendEntryRequestBehaviour())

class SendPaymentRequest(OneShotBehaviour):
    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        kiosk_exit_jid = cfg.get_kiosk_exit_jid(park_manager_jid)

        if self.agent.is_currently_parked():
            msg = Message(
                to=kiosk_exit_jid,
                metadata={"performative": "payment_request"},
                body=jsonpickle.encode({
                    "vehicle_id": self.agent.get_plate()
                })
            )

            await self.send(msg)
            self.agent.logger.info("Payment request sent to kiosk exit")

class RecvPaymentAmount(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "payment_amount" and cfg.identify(msg.sender) == "kiosk_exit"):
            msg_body = jsonpickle.decode(msg.body)
            amount = msg_body.get("amount")

            self.agent.logger.info(f"Payment amount received: {amount}€")

            self.agent.add_behaviour(SendPayment(amount))

class SendPayment(OneShotBehaviour):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        kiosk_exit_jid = cfg.get_kiosk_exit_jid(park_manager_jid)

        msg = Message(
            to=kiosk_exit_jid,
            metadata={"performative": "payment_done"},
            body=jsonpickle.encode({
                "vehicle_id": self.agent.get_plate(),
            })
        )
        await self.send(msg)
        self.agent.logger.success(f"Payment of {self.amount}€ sent to kiosk exit")

class SendExitRequest(OneShotBehaviour):
    async def run(self):
        park_manager_jid = cfg.get_park_jid(self.agent.get_location())
        barrier_exit_jid = cfg.get_barrier_exit_jid(park_manager_jid)

        if self.agent.is_currently_parked():
            msg = Message(
                to=barrier_exit_jid,
                metadata={"performative": "exit_request"},
                body=jsonpickle.encode({
                    "vehicle_id": self.agent.get_plate(),
                })
            )
            await self.send(msg)
            self.agent.logger.info("Exit request sent to barrier")

class RecvPaymentWarning(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "payment_warning" and cfg.identify(msg.sender) == "park_manager"):
            self.agent.logger.warning("Payment warning received from park manager")
            self.agent.add_behaviour(SendPaymentRequest())

class RecvPaymentConfirmation(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "payment_confirmed" and cfg.identify(msg.sender) == "park_manager"):
            self.agent.logger.success("Payment confirmed by park manager")
            self.agent.add_behaviour(SendExitRequest())

class VehicleRetryEntryRequestBehaviour(PeriodicBehaviour):
    async def run(self):
        if self.agent.is_waiting_at_park() and self.agent.get_entry_retries() <= 1:
            self.agent.add_behaviour(SendExitWaitingZoneRequest())
            self.agent.add_behaviour(SendEntryRequestBehaviour())
            self.agent.set_waiting(False)

            park_manager_jid = cfg.get_park_jid(self.agent.get_location())

            self.agent.logger.warning("Retrying entry request")
        
        elif self.agent.is_waiting_at_park() and self.agent.get_entry_retries() > 1:
            self.agent.add_behaviour(SendExitWaitingZoneRequest())
            self.agent.add_behaviour(SendRedirectRequest())
            self.agent.set_waiting(False)

            self.agent.logger.warning("Maximum retries reached, requesting redirect")



class ReceiveCanExitResponse(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "can_exit" and cfg.identify(msg.sender) == "park_manager"):
            self.agent.logger.success("Received confirmation to exit the park")

            self.agent.set_parked(False)

class ReceiveRedirectDenial(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        if (msg.metadata.get("performative") == "redirect_park_response_none" and cfg.identify(msg.sender) == "central_manager"):
            self.agent.logger.warning("Redirect denied by central manager, going to wait zone")

            self.agent.add_behaviour(WaitAtParkBehaviour())

