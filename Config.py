"""
Configuração central do sistema de estacionamento
Inspirado em: https://github.com/Katilho/Trabalho-ASM-2023-2024
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração central dos JIDs e domínio"""
    
    DOMAIN = os.getenv("DOMAIN", "localhost")
    PASSWORD = os.getenv("PASSWORD", "password123")
    
    # JIDs dos agentes
    manager_parque_jid = f"manager_parque@{DOMAIN}"
    barreira_saida_jid = f"barreira_saida@{DOMAIN}"
    kiosque_saida_jid = f"kiosque_saida@{DOMAIN}"
    kiosque_entrada_jid = f"kiosque_entrada@{DOMAIN}"
    central_manager_jid = f"central_manager@{DOMAIN}"
    location_jid = f"location@{DOMAIN}"
    zona_espera_jid = f"zona_espera@{DOMAIN}"
    
    @staticmethod
    def get_domain_name():
        """Retorna o domínio configurado"""
        return Config.DOMAIN
    
    @staticmethod
    def get_password():
        """Retorna a password configurada"""
        return Config.PASSWORD
    
    @staticmethod
    def get_manager_jid():
        """Retorna o JID do Manager Parque"""
        return Config.manager_parque_jid
    
    @staticmethod
    def get_barreira_saida_jid():
        """Retorna o JID da Barreira de Saída"""
        return Config.barreira_saida_jid
    
    @staticmethod
    def get_kiosque_saida_jid():
        """Retorna o JID do Kiosque de Saída"""
        return Config.kiosque_saida_jid
    
    @staticmethod
    def get_kiosque_entrada_jid():
        """Retorna o JID do Kiosque de Entrada"""
        return Config.kiosque_entrada_jid
    
    @staticmethod
    def get_central_manager_jid():
        """Retorna o JID do Central Manager"""
        return Config.central_manager_jid
    
    @staticmethod
    def get_location_jid():
        """Retorna o JID do Location"""
        return Config.location_jid
    
    @staticmethod
    def get_zona_espera_jid():
        """Retorna o JID da Zona de Espera"""
        return Config.zona_espera_jid
    
    @staticmethod
    def get_sensor_jid(sensor_id):
        """Retorna o JID de um sensor"""
        return f"{sensor_id}@{Config.DOMAIN}"
    
    @staticmethod
    def get_vehicle_jid(vehicle_id):
        """Retorna o JID de um veículo"""
        return f"{vehicle_id}@{Config.DOMAIN}"
    
    @staticmethod
    def get_jid_name(jid):
        """Extrai o nome do JID"""
        if isinstance(jid, str):
            return jid.split("@")[0]
        return str(jid).split("/")[0].split("@")[0]
    
    @staticmethod
    def stats_file_name():
        """Retorna o caminho do ficheiro de estatísticas"""
        return "resources/stats.json"
    
    @staticmethod
    def logs_file_name():
        """Retorna o caminho do ficheiro de logs"""
        return "resources/logs.txt"
