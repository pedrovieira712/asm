import asyncio
from Utils.init import init_agents, load_scenario
from Utils.interceptors.print_interceptor import PrintInterceptor
from Utils.log_formatter import print_separator, print_header, print_box
import argparse
import os
import sys
import time

async def main_tests(scenario_file):
    scenario = load_scenario(scenario_file) 
    expected_plates = set(v["plate"] for v in scenario.get("vehicles", []))

    # Cabeçalho do teste
    print_separator('═', width=100)
    print_header(f"    INICIANDO SIMULAÇÃO: {os.path.basename(scenario_file)}    ".center(100))
    print_separator('═', width=100)
    
    # Informações do cenário
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
    timeout_seconds = 45

    try:
        while True:
            await asyncio.sleep(1)
            if interceptor and interceptor.confirmed_plates >= expected_plates:
                sys.stdout = interceptor.original_stdout
                print()
                print_separator('═', width=100)
                print_header("    ✅ TESTE CONCLUÍDO COM SUCESSO!    ".center(100))
                print_separator('═', width=100)
                break

            if not interceptor and (time.time() - start_time) > timeout_seconds:
                print()
                print_separator('═', width=100)
                print_header("    ✅ TESTE CONCLUÍDO COM SUCESSO!    ".center(100))
                print_separator('═', width=100)
                break

    except KeyboardInterrupt:
        sys.stdout = interceptor.original_stdout if interceptor else sys.stdout
        print()
        print_separator('═', width=100)
        print_header("    ⚠️  INTERROMPIDO PELO UTILIZADOR    ".center(100))
        print_separator('═', width=100)
        print("\nA terminar os agentes...")

    for agent in agents:
        await agent.stop()



async def main_interface():
    print("Modo interface selecionado (ainda por implementar)")
    await asyncio.sleep(0)


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
    asyncio.run(main())