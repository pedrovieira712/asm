import asyncio
import os
import sys
from Utils.init import init_agents, load_scenario

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    print("=" * 60)
    print("       SISTEMA MULTI-AGENTE - GESTÃO DE PARQUES")
    print("=" * 60)
    print()

def show_main_menu():
    print("┌─────────────────────────────────────┐")
    print("│           MENU PRINCIPAL            │")
    print("├─────────────────────────────────────┤")
    print("│  1. Executar Cenário de Teste       │")
    print("│  2. Listar Cenários Disponíveis     │")
    print("│  3. Ver Configurações               │")
    print("│  4. Informações do Projeto          │")
    print("│  0. Sair                            │")
    print("└─────────────────────────────────────┘")
    print()

def list_scenarios():
    clear_screen()
    show_header()
    print(" CENÁRIOS DISPONÍVEIS:")
    print("-" * 40)
    
    scenarios_path = os.path.join(os.path.dirname(__file__), "inputs")
    scenarios = [f for f in os.listdir(scenarios_path) if f.endswith('.json')]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario}")
    
    print("-" * 40)
    input("\nPressione ENTER para voltar...")

def show_config():
    clear_screen()
    show_header()
    print("  CONFIGURAÇÕES ATUAIS:")
    print("-" * 40)
    
    from Config import Config
    print(f"  Domínio: {Config.DOMAIN}")
    print(f"  Fator de Aceleração: {Config.TIME_ACCELERATION_FACTOR}x")
    print(f"  Manager Central: {Config.manager_central_jid}")
    print("-" * 40)
    input("\nPressione ENTER para voltar...")

def show_info():
    clear_screen()
    show_header()
    print("  INFORMAÇÕES DO PROJETO:")
    print("-" * 40)
    print("  Disciplina: ASM - Agentes e Sistemas Multi-Agente")
    print("  Ano: 2025/2026")
    print("  Framework: SPADE 3.3.2")
    print()
    print("  Agentes implementados:")
    print("    • ManagerCentral")
    print("    • ManagerParque")
    print("    • KioskEntrada / KioskSaida")
    print("    • BarreiraEntrada / BarreiraSaida")
    print("    • ZonaEspera")
    print("    • Sensor")
    print("    • Veiculo")
    print("-" * 40)
    input("\nPressione ENTER para voltar...")

async def run_scenario():
    clear_screen()
    show_header()
    print(" EXECUTAR CENÁRIO:")
    print("-" * 40)
    
    scenarios_path = os.path.join(os.path.dirname(__file__), "inputs")
    scenarios = [f for f in os.listdir(scenarios_path) if f.endswith('.json')]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario}")
    
    print("  0. Voltar")
    print("-" * 40)
    
    try:
        choice = int(input("\nEscolha um cenário: "))
        if choice == 0:
            return
        if 1 <= choice <= len(scenarios):
            scenario_file = scenarios[choice - 1]
            print(f"\n  A iniciar cenário: {scenario_file}")
            print("   (Pressione Ctrl+C para parar)\n")
            
            scenario_path = os.path.join("inputs", scenario_file)
            agents = await init_agents(scenario_path)
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n\n  A parar agentes...")
                for agent in agents:
                    await agent.stop()
                print(" Agentes parados com sucesso!")
        else:
            print(" Opção inválida!")
    except ValueError:
        print(" Por favor, insira um número!")
    
    input("\nPressione ENTER para voltar...")

async def main_menu():
    while True:
        clear_screen()
        show_header()
        show_main_menu()
        
        try:
            choice = input("Escolha uma opção: ")
            
            if choice == "1":
                await run_scenario()
            elif choice == "2":
                list_scenarios()
            elif choice == "3":
                show_config()
            elif choice == "4":
                show_info()
            elif choice == "0":
                clear_screen()
                print(" Até breve!")
                sys.exit(0)
            else:
                print(" Opção inválida!")
                input("Pressione ENTER para continuar...")
        except KeyboardInterrupt:
            clear_screen()
            print("\nAté breve!")
            sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main_menu())