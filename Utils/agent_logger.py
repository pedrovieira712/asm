from Utils.log_formatter import LogFormatter, Colors


class AgentLogger:
    def __init__(self, agent_type, agent_id):
        self.agent_type = agent_type
        self.agent_id = agent_id
        self.formatter = LogFormatter()
    
    def info(self, message):
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'INFO'))
    
    def success(self, message):
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'SUCCESS'))
    
    def warning(self, message):
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'WARNING'))
    
    def error(self, message):
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'ERROR'))
    
    def debug(self, message):
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'DEBUG'))
    
    def separator(self, title=''):
        print(self.formatter.format_separator(title))

def create_vehicle_logger(vehicle_id):
    return AgentLogger('Vehicle', vehicle_id)


def create_park_manager_logger(park_id):
    return AgentLogger('Park Manager', park_id)


def create_kiosk_entry_logger(park_id):
    return AgentLogger('Entry Kiosk', park_id)


def create_kiosk_exit_logger(park_id):
    return AgentLogger('Exit Kiosk', park_id)


def create_barrier_logger(park_id):
    return AgentLogger('Barrier Exit', park_id)


def create_sensor_logger(sensor_id):
    return AgentLogger('Sensor', sensor_id)


def create_central_manager_logger():
    return AgentLogger('Central Manager', 'MAIN')


def create_location_logger():
    return AgentLogger('Location', 'SYS')


def create_wait_zone_logger(park_id):
    return AgentLogger('Wait Zone', park_id)

