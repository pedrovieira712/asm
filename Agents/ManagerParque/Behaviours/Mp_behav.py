from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from datetime import datetime
import jsonpickle
from Config import Config as cfg

class ReceiveRedirectVehicleRequestBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "redirect_vehicle_request" and cfg.identify(msg.sender) == "central_manager":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            vehicle_info = msg_body.get("vehicle_info", {})

            vehicle_type = vehicle_info.get("vehicle_type")
            user_type = vehicle_info.get("user_type")
            vehicle_height = vehicle_info.get("vehicle_height")

            self.agent.logger.info(f"Received redirect request for vehicle {vehicle_id}")

            if vehicle_type is not None and user_type is not None and vehicle_height is not None:
                is_available = self.agent.check_availability(vehicle_type, user_type, vehicle_height)

                self.agent.add_behaviour(
                    SendRedirectVehicleResponseBehaviour(vehicle_id, is_available, self.agent.location)
                )

class SendRedirectVehicleResponseBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id, is_available, park_location):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.is_available = is_available
        self.park_location = park_location

    async def run(self):
        central_manager_jid = cfg.get_central_manager_jid() 

        msg = Message(
            to=central_manager_jid, 
            metadata={"performative": "redirect_vehicle_response"},
            body=jsonpickle.encode({
                "vehicle_id": self.vehicle_id,
                "is_available": self.is_available,
                "park_location": self.park_location,
            })
        )

        await self.send(msg)
        self.agent.logger.info(f"Sent redirect response for vehicle {self.vehicle_id}: {'available' if self.is_available else 'not available'}")

class ReceiveEntryRequestBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "entry_request" and cfg.identify(msg.sender) == "kiosk_entry":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            vehicle_info = msg_body.get("vehicle_info", {})

            vehicle_type = vehicle_info.get("vehicle_type")
            user_type = vehicle_info.get("user_type")
            vehicle_height = vehicle_info.get("vehicle_height")

            is_available = self.agent.check_availability(vehicle_type, user_type, vehicle_height)

            self.agent.logger.info(f"Received entry request for vehicle {vehicle_id}")

            if is_available:
                free_spot = self.agent.get_free_spot(vehicle_type, user_type)
                if free_spot is not None:
                    self.agent.mark_spot_occupied(free_spot)
                    self.agent.record_payment(vehicle_id, False)
                    sensor_jid = self.agent.get_sensor_for_spot(free_spot)
                    self.agent.associate_vehicle_with_sensor(vehicle_id, sensor_jid)
                    self.agent.associate_vehicle_with_spot(vehicle_id, free_spot)
                    
                    if sensor_jid:
                        self.agent.add_behaviour(
                            SendSensorUpdateBehaviour(sensor_jid, free_spot, vehicle_id)
                        )
                    
                    self.agent.add_behaviour(
                        SendKioskEntryConfirmationBehaviour(vehicle_id, free_spot)
                    )

                    entry_time = datetime.now()
                    self.agent.record_entry_time(vehicle_id, entry_time)

                else:
                    self.agent.add_behaviour(
                        SendKioskEntryDenialBehaviour(vehicle_id)
                    )
            else:
                self.agent.add_behaviour(
                    SendKioskEntryDenialBehaviour(vehicle_id)
                )

        
class SendSensorUpdateBehaviour(OneShotBehaviour):
    def __init__(self, sensor_jid, spot_id, vehicle_id):
        super().__init__()
        self.sensor_jid = sensor_jid
        self.spot_id = spot_id
        self.vehicle_id = vehicle_id

    async def run(self):
        msg = Message(
            to=self.sensor_jid,
            metadata={"performative": "mark_spot"},
            body=jsonpickle.encode({
                "vehicle_id": self.vehicle_id
            })
        )
        await self.send(msg)
        self.agent.logger.info(f"Sensor notified to mark spot {self.spot_id} for vehicle {self.vehicle_id}")

class SendKioskEntryConfirmationBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id, spot_id):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.spot_id = spot_id

    async def run(self):
        kiosk_entry_jid = cfg.get_kiosk_entry_jid(str(self.agent.jid))
        msg = Message(
            to=kiosk_entry_jid,
            metadata={"performative": "entry_response"},
            body=jsonpickle.encode({
                "state": True,
                "vehicle_id": self.vehicle_id,
            })
        )
        await self.send(msg)
        self.agent.logger.success(f"Entry authorized for vehicle {self.vehicle_id} at spot {self.spot_id}")

class SendKioskEntryDenialBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        kiosk_entry_jid = cfg.get_kiosk_entry_jid(str(self.agent.jid))
        msg = Message(
            to=kiosk_entry_jid,
            metadata={"performative": "entry_response"},
            body=jsonpickle.encode({
                "state": False,
                "vehicle_id": self.vehicle_id,
            })
        )
        await self.send(msg)
        self.agent.logger.warning(f"Entry denied for vehicle {self.vehicle_id}")

class ReceivePaymentConfirmationBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "payment_confirmed" and cfg.identify(msg.sender) == "kiosk_exit":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            self.agent.record_payment(vehicle_id, True)

            self.agent.logger.success(f"Payment confirmed for vehicle {vehicle_id}")
            
            self.agent.add_behaviour(
                SendPaymentConfirmationVehicle(vehicle_id)
            )

class SendPaymentConfirmationVehicle(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        vehicle_jid = cfg.get_vehicle_jid(self.vehicle_id)
        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "payment_confirmed"},
        )

        await self.send(msg)
        self.agent.logger.info(f"Payment confirmation sent to vehicle {self.vehicle_id}")

class ReceivePaymentVerificationBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "send_request_payment_check" and cfg.identify(msg.sender) == "barrier_exit":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            
            has_paid = self.agent.has_paid(vehicle_id)

            self.agent.logger.info(f"Payment verification for vehicle {vehicle_id}")

            if has_paid:
                self.agent.add_behaviour(
                    SendBarrierExitOpen(vehicle_id)
                )

                self.agent.add_behaviour(
                    SendVehicleCanExit(vehicle_id)
                )

                self.agent.rem_payment_record(vehicle_id)
                self.agent.rem_sensor_for_vehicle(vehicle_id)
                self.agent.rem_entry_time(vehicle_id)
                self.agent.mark_spot_free(self.agent.get_vehicle_spot(vehicle_id))
                self.agent.rem_vehicle_spot_association(vehicle_id)
            
            else:
                self.agent.add_behaviour(
                    SendPaymentWarning(vehicle_id)
                )

class SendPaymentWarning(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        vehicle_jid = cfg.get_vehicle_jid(self.vehicle_id)
        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "payment_warning"},
            body=jsonpickle.encode({"vehicle_id": self.vehicle_id})
        )

        await self.send(msg)
        self.agent.logger.warning(f"Payment warning sent to vehicle {self.vehicle_id}")

class SendBarrierExitOpen(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        barrier_exit_jid = cfg.get_barrier_exit_jid(str(self.agent.jid))
        sensor_jid = self.agent.get_sensor_for_vehicle(self.vehicle_id)

        msg = Message(
            to=barrier_exit_jid,
            metadata={"performative": "confirm_payment"},
            body=jsonpickle.encode({
                "sensor_jid": sensor_jid,
                "vehicle_id": self.vehicle_id,
            })
        )

        await self.send(msg)
        self.agent.logger.success(f"Payment confirmed for vehicle {self.vehicle_id}, barrier exit opened")

class SendVehicleCanExit(OneShotBehaviour):
    def __init__(self, vehicle_id):
        super().__init__()
        self.vehicle_id = vehicle_id

    async def run(self):
        vehicle_jid = cfg.get_vehicle_jid(self.vehicle_id)
        msg = Message(
            to=vehicle_jid,
            metadata={"performative": "can_exit"},
            body=jsonpickle.encode({"vehicle_id": self.vehicle_id})
        )

        await self.send(msg)
        self.agent.logger.info(f"Vehicle {self.vehicle_id} notified it can exit")

class ReceiveEntrytimeRequestBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg is None:
            return

        performative = msg.metadata.get("performative")

        if performative == "request_entry_time" and cfg.identify(msg.sender) == "kiosk_exit":
            msg_body = jsonpickle.decode(msg.body)

            vehicle_id = msg_body.get("vehicle_id")
            entry_time = self.agent.get_entry_time(vehicle_id)

            self.agent.logger.info(f"Entry time requested for vehicle {vehicle_id}")

            self.agent.add_behaviour(
                SendEntrytimeResponseBehaviour(vehicle_id, entry_time)
            )

class SendEntrytimeResponseBehaviour(OneShotBehaviour):
    def __init__(self, vehicle_id, entry_time):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.entry_time = entry_time

    async def run(self):
        kiosk_exit_jid = cfg.get_kiosk_exit_jid(str(self.agent.jid))

        msg = Message(
            to=kiosk_exit_jid,
            metadata={"performative": "entry_time_response"},
            body=jsonpickle.encode({
                "vehicle_id": self.vehicle_id,
                "entry_time": self.entry_time,
            })
        )

        await self.send(msg)
        self.agent.logger.success(f"Entry time response sent for vehicle {self.vehicle_id}")