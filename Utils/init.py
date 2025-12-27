import asyncio
from Config import Config as cfg

from Agents.ManagerParque.ManagerParque import ManagerParque
from Agents.Barreira_Saida.Barreira_saida import BarreiraSaida
from Agents.Kiosque_Saida.Kiosque_Saida import Kiosque_saida
from Agents.Kiosque_Entrada.Kiosque_Entrada import Kiosque_Entrada
from Agents.CentralManager.CentralManager import CentralManager
from Agents.Location.Location import Location
from Agents.Sensor.Sensor import Sensor
from Agents.Vehicle.Vehicle import Vehicle
from Agents.ZonadeEspera.zonadeespera import ZonadeEspera

PASSWORD = cfg.get_password()

async def init_agents():
    agents = []

    central = CentralManager(jid=cfg.get_central_manager_jid(), password=PASSWORD)
    location_agent = Location(jid=cfg.get_location_manager_jid(), password=PASSWORD)
    agents.extend([central, location_agent])

    park_locations = [1, 10]  

    for i, loc in enumerate(park_locations, start=1):
        park_id = f"P{i}"
        
        manager_jid = cfg.get_park_jid(loc) 

        manager = ManagerParque(
            jid=manager_jid,
            password=PASSWORD,
            park_id=park_id,
            capacity=1,
            max_height=2.5 if i == 1 else 3.0,
            location=loc
        )
        manager.add_parking_spot(
            spot_id="L1",
            allowed_vehicle_types=["car", "motorcycle", "truck", "caravan", "bus"],  
            allowed_user_types=["normal", "pregnant", "reduced_mobility", "elderly"]  
        )

        entrada_jid = cfg.get_kiosk_entry_jid(manager_jid)
        saida_jid = cfg.get_kiosk_exit_jid(manager_jid)
        barreira_jid = cfg.get_barrier_exit_jid(manager_jid)
        espera_jid = cfg.get_wait_zone_jid(manager_jid)
        sensor_jid = cfg.get_sensor_jid(manager_jid, spot_id="L1")

        entrada = Kiosque_Entrada(jid=entrada_jid, password=PASSWORD, park_jid=manager_jid)
        saida = Kiosque_saida(jid=saida_jid, password=PASSWORD, park_jid=manager_jid,
                              tarifa_minuto=0.05, hora_fecho="23:00", multa_fixa=20.0)
        barreira = BarreiraSaida(jid=barreira_jid, password=PASSWORD, park_jid=manager_jid)
        espera = ZonadeEspera(jid=espera_jid, password=PASSWORD, park_jid=manager_jid)
        sensor = Sensor(jid=sensor_jid, password=PASSWORD, id_lugar="L1", park_jid=manager_jid)

        manager.add_sensor_for_spot("L1", sensor_jid)
        location_agent.add_ParkLocation(manager_jid, loc)
        agents.extend([manager, entrada, saida, barreira, espera, sensor])

    v1 = Vehicle(
        jid=cfg.get_vehicle_jid("AA-11-BB"),
        password=PASSWORD,
        vehicle_type="car",
        user_type="normal",
        location=1,        
        redirect=True,
        vehicle_height=1.8,
        plate="AA-11-BB",
        skip_payment=False
    )

    v2 = Vehicle(
        jid=cfg.get_vehicle_jid("CC-22-DD"),
        password=PASSWORD,
        vehicle_type="car",
        user_type="normal",
        location=10,         
        redirect=True,
        vehicle_height=1.7,
        plate="CC-22-DD",
        skip_payment=True
    )

    agents.extend([v1, v2])

    for agent in agents:
        await agent.start(auto_register=True)
        print(f"[INIT] Agente iniciado: {agent.jid}")

    return agents