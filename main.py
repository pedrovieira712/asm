import asyncio
from Utils.init import init_agents
import sys  

async def main():
    if len(sys.argv) > 1:
        scenario_file = sys.argv[1]
    
    agents = await init_agents(scenario_file)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\nA terminar os agentes...")
        for agent in agents:
            await agent.stop()
        print("Todos os agentes parados. Adeus!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEncerramento forçado.")