"""
Logger específico para agentes do sistema multi-agente.
Fornece métodos convenientes para logging formatado.
"""

from Utils.log_formatter import LogFormatter, Colors


class AgentLogger:
    """Logger para agentes individuais com formatação automática"""
    
    def __init__(self, agent_type, agent_id):
        """
        Inicializa o logger para um agente específico.
        
        Args:
            agent_type: Tipo do agente (Vehicle, Park Manager, etc.)
            agent_id: Identificador único do agente
        """
        self.agent_type = agent_type
        self.agent_id = agent_id
        self.formatter = LogFormatter()
    
    def info(self, message):
        """Log de informação"""
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'INFO'))
    
    def success(self, message):
        """Log de sucesso"""
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'SUCCESS'))
    
    def warning(self, message):
        """Log de aviso"""
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'WARNING'))
    
    def error(self, message):
        """Log de erro"""
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'ERROR'))
    
    def debug(self, message):
        """Log de debug"""
        print(self.formatter.format_log(self.agent_type, self.agent_id, message, 'DEBUG'))
    
    def separator(self, title=''):
        """Imprime um separador"""
        print(self.formatter.format_separator(title))


# Funções auxiliares para criar loggers rapidamente
def create_vehicle_logger(vehicle_id):
    """Cria um logger para veículo"""
    return AgentLogger('Vehicle', vehicle_id)


def create_park_manager_logger(park_id):
    """Cria um logger para gestor de parque"""
    return AgentLogger('Park Manager', park_id)


def create_kiosk_entry_logger(park_id):
    """Cria um logger para quiosque de entrada"""
    return AgentLogger('Entry Kiosk', park_id)


def create_kiosk_exit_logger(park_id):
    """Cria um logger para quiosque de saída"""
    return AgentLogger('Exit Kiosk', park_id)


def create_barrier_logger(park_id):
    """Cria um logger para barreira"""
    return AgentLogger('Barrier Exit', park_id)


def create_sensor_logger(sensor_id):
    """Cria um logger para sensor"""
    return AgentLogger('Sensor', sensor_id)


def create_central_manager_logger():
    """Cria um logger para gestor central"""
    return AgentLogger('Central Manager', 'MAIN')


def create_location_logger():
    """Cria um logger para gestor de localizações"""
    return AgentLogger('Location', 'SYS')


def create_wait_zone_logger(park_id):
    """Cria um logger para zona de espera"""
    return AgentLogger('Wait Zone', park_id)


# Exemplo de uso em comentário
"""
# No início do ficheiro do agente:
from Utils.agent_logger import create_vehicle_logger

# Na classe do agente:
class Vehicle:
    def __init__(self, jid, password, vehicle_type, plate, ...):
        super().__init__(jid, password)
        self.logger = create_vehicle_logger(plate)
        # ... resto da inicialização
    
    def some_method(self):
        self.logger.info("Payment request sent to kiosk exit")
        self.logger.success("Payment confirmed by park manager")
        self.logger.warning("Park is full, redirecting...")
        self.logger.error("Failed to connect to park manager")
"""
