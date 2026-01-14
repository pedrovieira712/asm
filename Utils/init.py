import asyncio
import json
from Config import Config as cfg

from Agents.ManagerParque.managerParque import ManagerParque
from Agents.Barreira_Saida.Barreira_saida import BarreiraSaida
from Agents.Kiosque_Saida.Kiosque_Saida import Kiosque_saida
from Agents.Kiosque_Entrada.Kiosque_Entrada import Kiosque_Entrada
from Agents.CentralManager.CentralManager import CentralManager
from Agents.Location.Location import Location
from Agents.Sensor.sensor import Sensor
from Agents.Vehicle.Vehicle import Vehicle
from Agents.ZonadeEspera.zonadeespera import ZonadeEspera

PASSWORD = cfg.get_password()


def load_scenario(filename="scenario.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


async def init_agents(scenario_file="scenario.json"):
    agents = []

    central = CentralManager(jid=cfg.get_central_manager_jid(), password=PASSWORD)
    location_agent = Location(jid=cfg.get_location_manager_jid(), password=PASSWORD)
    agents.extend([central, location_agent])

    scenario = load_scenario(scenario_file)

    for park_config in scenario["parks"]:
        loc = tuple(park_config["location"])
        park_id = park_config["id"]

        manager_jid = cfg.get_park_jid(loc)

        manager = ManagerParque(
            jid=manager_jid,
            password=PASSWORD,
            park_id=park_id,
            capacity=park_config.get("capacity", 10),
            max_height=park_config.get("max_height", 3.0),
            location=loc
        )

        spots_list = park_config.get("spots", [{"spot_id": "L1"}])
        for spot in spots_list:
            manager.add_parking_spot(
                spot_id=spot["spot_id"],
                allowed_vehicle_types=spot.get("allowed_vehicle_types", ["car", "motorcycle", "truck", "caravan", "bus"]),
                allowed_user_types=spot.get("allowed_user_types", ["normal", "pregnant", "reduced_mobility", "elderly"])
            )

        entrada_jid = cfg.get_kiosk_entry_jid(manager_jid)
        saida_jid = cfg.get_kiosk_exit_jid(manager_jid)
        barreira_jid = cfg.get_barrier_exit_jid(manager_jid)
        espera_jid = cfg.get_wait_zone_jid(manager_jid)

        entrada = Kiosque_Entrada(jid=entrada_jid, password=PASSWORD, park_jid=manager_jid)
        saida = Kiosque_saida(
            jid=saida_jid,
            password=PASSWORD,
            park_jid=manager_jid,
            tarifa_minuto=park_config.get("tarifa_minuto", 0.05),
            hora_fecho=park_config.get("hora_fecho", "23:00"),
            multa_fixa=park_config.get("multa_fixa", 20.0)
        )
        barreira = BarreiraSaida(jid=barreira_jid, password=PASSWORD, park_jid=manager_jid)
        espera = ZonadeEspera(jid=espera_jid, password=PASSWORD, park_jid=manager_jid)

        sensors_for_park = []
        for spot in spots_list:
            sensor_jid = cfg.get_sensor_jid(manager_jid, spot_id=spot["spot_id"])
            sensor = Sensor(
                jid=sensor_jid,
                password=PASSWORD,
                id_lugar=spot["spot_id"],
                park_jid=manager_jid
            )
            manager.add_sensor_for_spot(spot["spot_id"], sensor_jid)
            sensors_for_park.append(sensor)

        location_agent.add_ParkLocation(manager_jid, loc)

        agents.extend([manager, entrada, saida, barreira, espera])
        agents.extend(sensors_for_park)  

    for veh_config in scenario.get("vehicles", []):
        vehicle = Vehicle(
            jid=cfg.get_vehicle_jid(veh_config["plate"]),
            password=PASSWORD,
            vehicle_type=veh_config["vehicle_type"],
            user_type=veh_config["user_type"],
            location=tuple(veh_config["location"]),
            redirect=veh_config.get("redirect", True),
            vehicle_height=veh_config.get("vehicle_height", 2.9),
            plate=veh_config["plate"],
            skip_payment=veh_config.get("skip_payment", False)
        )
        agents.append(vehicle)

    for agent in agents:
        await agent.start(auto_register=True)
        print(f"[INIT] Agente iniciado: {agent.jid}")

    return agents