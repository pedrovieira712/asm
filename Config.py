import os
from dotenv import load_dotenv

load_dotenv()

def location_to_str(location):
    lat, lon = location
    lat_str = f"{lat}".rstrip('0').rstrip('.') 
    lon_str = f"{lon}".rstrip('0').rstrip('.')

    return f"{lat_str}_{lon_str.replace('-', 'm')}"


class Config:    
    DOMAIN = os.getenv("DOMAIN", "localhost")
    PASSWORD = os.getenv("PASSWORD", "password123")

    TIME_ACCELERATION_FACTOR = 60
    
    manager_central_jid = f"central_manager@{DOMAIN}"
    
    @staticmethod
    def get_domain_name():
        return Config.DOMAIN
    
    @staticmethod
    def get_time_factor():
        return Config.TIME_ACCELERATION_FACTOR
    
    @staticmethod
    def get_password():
        return Config.PASSWORD
    
    @staticmethod
    def get_jid_name(jid):
        if isinstance(jid, str):
            return jid.split("@")[0]
        
    @staticmethod
    def get_central_manager_jid():
        return Config.manager_central_jid

    @staticmethod
    def get_park_jid(location):
        loc_str = location_to_str(location)
        return f"park_manager_{loc_str}@{Config.DOMAIN}"
    
    @staticmethod
    def get_barrier_exit_jid(park_jid):
        park_name = Config.get_jid_name(park_jid) 
        return f"barrier_exit_{park_name}@{Config.DOMAIN}"

    @staticmethod
    def get_kiosk_entry_jid(park_jid):
        park_name = Config.get_jid_name(park_jid)
        return f"kiosk_entry_{park_name}@{Config.DOMAIN}"

    @staticmethod
    def get_kiosk_exit_jid(park_jid):
        park_name = Config.get_jid_name(park_jid)
        return f"kiosk_exit_{park_name}@{Config.DOMAIN}"

    @staticmethod
    def get_wait_zone_jid(park_jid):
        park_name = Config.get_jid_name(park_jid)
        return f"wait_zone_{park_name}@{Config.DOMAIN}"

    @staticmethod
    def get_sensor_jid(park_jid, spot_id):
        park_name = Config.get_jid_name(park_jid)
        return f"sensor_{spot_id}_{park_name}@{Config.DOMAIN}"
    
    @staticmethod
    def get_location_manager_jid():
        return f"location_manager@{Config.DOMAIN}"

    
    @staticmethod
    def get_vehicle_jid(vehicle_id):
        return f"vehicle_{vehicle_id}@{Config.DOMAIN}"
    
    @staticmethod
    def identify(jid):

        str_jid = str(jid)

        if str_jid.startswith("vehicle"):
            return "vehicle"
        elif str_jid.startswith("kiosk_entry"):
            return "kiosk_entry"
        elif str_jid.startswith("barrier_exit"):
            return "barrier_exit"
        elif str_jid.startswith("kiosk_exit"):
            return "kiosk_exit"
        elif str_jid.startswith("park_manager"):
            return "park_manager"
        elif str_jid.startswith("wait_zone"):
            return "wait_zone"
        elif str_jid.startswith("sensor"):
            return "sensor"
        elif str_jid.startswith("central_manager"):
            return "central_manager"
        elif str_jid.startswith("location_manager"):
            return "location_manager"
        else:
            return "unknown"

    @staticmethod
    def stats_file_name():
        return "resources/stats.json"
    
    @staticmethod
    def logs_file_name():
        return "resources/logs.txt"
