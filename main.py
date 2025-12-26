"""
Sistema de Gestão de Estacionamento Multi-Agente
Main - Inicia todos os agentes e coordena a comunicação
"""
import asyncio
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, 'Agents')

# Imports dos agentes
from Barreira_Saida.Barreira_saida import BarreiraSaida
from Kiosque_Saida.Kiosque_Saida import Kiosque_saida
from Kiosque_Entrada.Kiosque_Entrada import Kiosque_Entrada
from Vehicle.Vehicle import Vehicle
from CentralManager.CentralManager import CentralManager
from Location.Location import Location
from ManagerParque.managerParque import ManagerParque
from Sensor.sensor import Sensor
from ZonadeEspera.zonadeespera import ZonadeEspera

# Configuração e utilitários
from Config import Config as cfg
from Utils.Prints import print_c, print_error, print_warning, print_success, print_info

# Configuração
DOMAIN = cfg.get_domain_name()
PASSWORD = cfg.get_password()

# JIDs dos agentes
JIDS = {
    "manager_parque": cfg.get_manager_jid(),
    "barreira_saida": cfg.get_barreira_saida_jid(),
    "kiosque_saida": cfg.get_kiosque_saida_jid(),
    "kiosque_entrada": cfg.get_kiosque_entrada_jid(),
    "central_manager": cfg.get_central_manager_jid(),
    "location": cfg.get_location_jid(),
    "sensor_lugar1": cfg.get_sensor_jid("sensor_lugar1"),
    "sensor_saida": cfg.get_sensor_jid("sensor_saida"),
    "zona_espera": cfg.get_zona_espera_jid(),
    "vehicle1": cfg.get_vehicle_jid("vehicle1"),
}

async def setup_agents():
    """Cria e configura todos os agentes"""
    print_c("=" * 70, "cyan")
    print_c("🚗 SISTEMA DE GESTÃO DE ESTACIONAMENTO MULTI-AGENTE", "bright_cyan")
    print_c("=" * 70, "cyan")
    
    agents = {}
    
    try:
        # 1. Manager Parque
        print("\n[1/9] Criando ManagerParque...")
        manager_parque = ManagerParque(
            jid=JIDS["manager_parque"],
            password=PASSWORD,
            park_id="P1",
            capacity=10,
            max_height=2.5
        )
        agents["manager_parque"] = manager_parque
        print("✅ ManagerParque criado")
        
        # 2. Barreira Saída
        print("\n[2/9] Criando BarreiraSaida...")
        barreira_saida = BarreiraSaida(
            jid=JIDS["barreira_saida"],
            password=PASSWORD
        )
        # Configurar JIDs necessários
        barreira_saida.manager_jid = JIDS["manager_parque"]
        barreira_saida.sensor_jid = JIDS["sensor_saida"]
        agents["barreira_saida"] = barreira_saida
        print("✅ BarreiraSaida criada")
        
        # 3. Kiosque Saída
        print("\n[3/9] Criando KiosqueSaida...")
        kiosque_saida = Kiosque_saida(
            jid=JIDS["kiosque_saida"],
            password=PASSWORD
        )
        kiosque_saida.manager_jid = JIDS["manager_parque"]
        agents["kiosque_saida"] = kiosque_saida
        print("✅ KiosqueSaida criado")
        
        # 4. Kiosque Entrada
        print("\n[4/9] Criando KiosqueEntrada...")
        kiosque_entrada = Kiosque_Entrada(
            jid=JIDS["kiosque_entrada"],
            password=PASSWORD,
            park_id="P1"
        )
        kiosque_entrada.manager_jid = JIDS["manager_parque"]
        kiosque_entrada.quiosque_saida_jid = JIDS["kiosque_saida"]
        kiosque_entrada.central_manager_jid = JIDS["central_manager"]
        agents["kiosque_entrada"] = kiosque_entrada
        print("✅ KiosqueEntrada criado")
        
        # 5. Central Manager
        print("\n[5/9] Criando CentralManager...")
        central_manager = CentralManager(
            jid=JIDS["central_manager"],
            password=PASSWORD
        )
        central_manager.location_jid = JIDS["location"]
        agents["central_manager"] = central_manager
        print("✅ CentralManager criado")
        
        # 6. Location
        print("\n[6/9] Criando Location...")
        location = Location(
            jid=JIDS["location"],
            password=PASSWORD
        )
        # Adiciona parques disponíveis
        location.park_locations = {
            JIDS["manager_parque"]: {"nome": "Parque 1", "distancia": 0},
        }
        agents["location"] = location
        print("✅ Location criado")
        
        # 7. Sensores
        print("\n[7/9] Criando Sensores...")
        sensor_lugar = Sensor(
            jid=JIDS["sensor_lugar1"],
            password=PASSWORD,
            tipo_sensor="LUGAR",
            id_lugar="L1"
        )
        sensor_saida = Sensor(
            jid=JIDS["sensor_saida"],
            password=PASSWORD,
            tipo_sensor="SAIDA",
            id_lugar=None
        )
        agents["sensor_lugar1"] = sensor_lugar
        agents["sensor_saida"] = sensor_saida
        print("✅ Sensores criados")
        
        # 8. Zona de Espera
        print("\n[8/9] Criando ZonadeEspera...")
        zona_espera = ZonadeEspera(
            jid=JIDS["zona_espera"],
            password=PASSWORD
        )
        agents["zona_espera"] = zona_espera
        print("✅ ZonadeEspera criada")
        
        # 9. Veículo de teste
        print("\n[9/9] Criando Vehicle...")
        vehicle = Vehicle(
            jid=JIDS["vehicle1"],
            password=PASSWORD,
            vehicle_type="carro",
            user_type="normal"
        )
        vehicle.central_manager_jid = JIDS["central_manager"]
        agents["vehicle1"] = vehicle
        print("✅ Vehicle criado")
        
        return agents
        
    except Exception as e:
        print(f"\n❌ ERRO ao criar agentes: {e}")
        return None

async def start_all_agents(agents):
    """Inicia todos os agentes"""
    print("\n" + "=" * 70)
    print("🚀 INICIANDO TODOS OS AGENTES...")
    print("=" * 70)
    
    for name, agent in agents.items():
        try:
            await agent.start()
            print(f"✅ {name} iniciado")
        except Exception as e:
            print(f"❌ Erro ao iniciar {name}: {e}")
    
    print("\n✅ Todos os agentes iniciados!")

async def stop_all_agents(agents):
    """Para todos os agentes"""
    print("\n" + "=" * 70)
    print("🛑 PARANDO TODOS OS AGENTES...")
    print("=" * 70)
    
    for name, agent in agents.items():
        try:
            await agent.stop()
            print(f"✅ {name} parado")
        except Exception as e:
            print(f"❌ Erro ao parar {name}: {e}")

async def main():
    print("\n⚠️  CERTIFICA-TE QUE:")
    print("   1. Openfire está a correr")
    print("   2. Criaste os utilizadores no Openfire Admin:")
    print("      - manager_parque")
    print("      - barreira_saida")
    print("      - kiosque_saida")
    print("      - kiosque_entrada")
    print("      - central_manager")
    print("      - location")
    print("      - sensor_lugar1")
    print("      - sensor_saida")
    print("      - zona_espera")
    print("      - vehicle1")
    print("   3. Todos com password: password123")
    print("\n   Pressiona Enter para continuar...\n")
    input()
    
    # Criar agentes
    agents = await setup_agents()
    
    if agents is None:
        print("\n❌ Falha ao criar agentes. Abortando...")
        return
    
    # Iniciar agentes
    await start_all_agents(agents)
    
    print("\n" + "=" * 70)
    print("🎯 SISTEMA EM EXECUÇÃO")
    print("=" * 70)
    print("\nOs agentes estão a correr e prontos para comunicar!")
    print("\nOpções:")
    print("  - Pressiona 's' para mostrar status")
    print("  - Pressiona 'q' para sair")
    print("=" * 70)
    
    # Manter sistema a correr
    try:
        while True:
            await asyncio.sleep(1)
            
            # Verifica se o utilizador quer sair (simplificado)
            # Em produção, usarias threading ou aioconsole para input assíncrono
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupção detetada (Ctrl+C)")
    
    # Parar agentes
    await stop_all_agents(agents)
    
    print("\n" + "=" * 70)
    print("👋 SISTEMA ENCERRADO")
    print("=" * 70)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🔥 SISTEMA DE ESTACIONAMENTO INTELIGENTE")
    print("=" * 70)
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
