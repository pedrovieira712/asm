import asyncio
from Utils.init import init_agents, load_scenario
from Utils.interceptors.print_interceptor import PrintInterceptor
from Utils.log_formatter import print_separator, print_header, print_box
import argparse
import os
import sys
import time


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

_active_agents = []

async def cleanup_all_agents():
    global _active_agents
    if _active_agents:
        print("\nA parar agentes...")
        for agent in _active_agents:
            try:
                await agent.stop()
            except Exception:
                pass
        _active_agents.clear()
    
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

async def run_scenario():
    global _active_agents
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
            
            scenario = load_scenario(scenario_path)
            expected_plates = set(v["plate"] for v in scenario.get("vehicles", []))
            
            interceptor = None
            if "scenario_test_all" in scenario_file:
                interceptor = PrintInterceptor(expected_plates)
                sys.stdout = interceptor
            
            agents = await init_agents(scenario_path)
            _active_agents = agents 
            start_time = time.time()
            timeout_seconds = 45
            
            try:
                while True:
                    await asyncio.sleep(1)
                    
                    if interceptor and interceptor.confirmed_plates >= expected_plates:
                        sys.stdout = interceptor.original_stdout
                        print("\nCenário concluído com sucesso!")
                        break
                    
                    if not interceptor and (time.time() - start_time) > timeout_seconds:
                        print("\nCenário concluído com sucesso!")
                        break
                        
            except KeyboardInterrupt:
                sys.stdout = interceptor.original_stdout if interceptor else sys.stdout
                print("\n\n  A parar agentes...")
            finally:
                for agent in agents:
                    try:
                        await agent.stop()
                    except Exception:
                        pass
                _active_agents.clear()
                print("Agentes parados com sucesso!")
        else:
            print("Opção inválida!")
    except ValueError:
        print("Por favor, insira um número!")
    except KeyboardInterrupt:
        print("\n\nOperação cancelada.")
        pass
    
    input("Pressione ENTER para voltar...")

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
            elif choice == "0":
                clear_screen()
                print("Até breve!")
                await cleanup_all_agents()
                sys.exit(0)
            else:
                print(" Opção inválida!")
                input("Pressione ENTER para continuar...")
        except KeyboardInterrupt:
            clear_screen()
            print("\nAté breve!")
            await cleanup_all_agents()
            sys.exit(0)

async def main_tests(scenario_file):
    scenario = load_scenario(scenario_file) 
    expected_plates = set(v["plate"] for v in scenario.get("vehicles", []))

    print_header(f"INICIANDO SIMULAÇÃO: {os.path.basename(scenario_file)}")
    
    info_lines = [
        f"Parques: {len(scenario.get('parks', []))}",
        f"Veículos: {len(scenario.get('vehicles', []))}",
        f"Matrículas esperadas: {', '.join(expected_plates)}"
    ]
    print_box(info_lines, "Informações do Cenário")
    print_separator(width=100)
    print()

    interceptor = None
    if "scenario_test_all" in scenario_file:
        interceptor = PrintInterceptor(expected_plates)
        sys.stdout = interceptor

    agents = await init_agents(scenario_file)
    start_time = time.time()
    timeout_seconds = 60

    try:
        while True:
            await asyncio.sleep(1)
            if interceptor and interceptor.confirmed_plates >= expected_plates:
                sys.stdout = interceptor.original_stdout
                print()
                print_header("TESTE CONCLUÍDO COM SUCESSO!")
                break

            if not interceptor and (time.time() - start_time) > timeout_seconds:
                print()
                print_header("TESTE CONCLUÍDO COM SUCESSO!")
                break

    except KeyboardInterrupt:
        sys.stdout = interceptor.original_stdout if interceptor else sys.stdout
        print()
        print_header("INTERROMPIDO PELO UTILIZADOR")
        print("\nA terminar os agentes...")

    for agent in agents:
        await agent.stop()



async def main_interface():
    await main_menu()


async def main():
    parser = argparse.ArgumentParser(description="Executar simulação")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-ts",
        nargs=1,
        metavar="SCENARIO",
        help="Executar testes simples com cenário (ex: scenario_basic.json)"
    )

    group.add_argument(
        "-i",
        action="store_true",
        help="Executar modo interface"
    )

    args = parser.parse_args()

    if args.ts:
        scenario_name = args.ts[0]
        scenario_file = os.path.join("Inputs", scenario_name)

        if not os.path.isfile(scenario_file):
            parser.error(f"O ficheiro '{scenario_name}' não existe em 'Inputs/'")

        await main_tests(scenario_file)

 
    elif args.i:
        await main_interface()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nPrograma terminado.")
        sys.exit(0)