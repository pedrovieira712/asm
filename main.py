import asyncio
from Utils.init import init_agents  

async def main():
    print("A iniciar o sistema multi-agente com 2 parques (1 lugar cada) e 2 veículos...\n")
    
    agents = await init_agents()
    
    print("\nTodos os agentes estão a correr!")
    print("Observa os prints abaixo para ver as interações em tempo real.")
    print("\n----------------------------------------------------------------\n")
    print("(Podes parar com Ctrl+C)\n")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\nA terminar os agentes...")
        for agent in agents:
            await agent.stop()
        print("Todos os agentes parados. Adeus!")

if __name__ == "__main__":
    asyncio.run(main())