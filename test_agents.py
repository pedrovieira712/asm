"""
Script de teste simples para verificar se os agentes iniciam sem erros
"""
import asyncio
import sys
sys.path.insert(0, 'Agents')

async def test_agents():
    print("=" * 60)
    print("TESTE DE INICIALIZAÇÃO DOS AGENTES")
    print("=" * 60)
    
    try:
        # Teste 1: Importar Barreira_Saida
        print("\n[1/6] Testando Barreira_Saida...")
        from Barreira_Saida.Barreira_saida import BarreiraSaida
        print("✅ Barreira_Saida importada com sucesso")
        
        # Teste 2: Importar Kiosque_Saida
        print("\n[2/6] Testando Kiosque_Saida...")
        from Kiosque_Saida.Kiosque_Saida import Kiosque_saida
        print("✅ Kiosque_Saida importada com sucesso")
        
        # Teste 3: Importar Kiosque_Entrada
        print("\n[3/6] Testando Kiosque_Entrada...")
        from Kiosque_Entrada.Kiosque_Entrada import Kiosque_Entrada
        print("✅ Kiosque_Entrada importada com sucesso")
        
        # Teste 4: Importar Vehicle
        print("\n[4/6] Testando Vehicle...")
        from Vehicle.Vehicle import Vehicle
        print("✅ Vehicle importado com sucesso")
        
        # Teste 5: Importar CentralManager
        print("\n[5/6] Testando CentralManager...")
        from CentralManager.CentralManager import CentralManager
        print("✅ CentralManager importado com sucesso")
        
        # Teste 6: Importar Location
        print("\n[6/6] Testando Location...")
        from Location.Location import Location
        print("✅ Location importado com sucesso")
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS AGENTES IMPORTADOS COM SUCESSO!")
        print("=" * 60)
        
        # Teste de criação de instância (sem iniciar)
        print("\n[TESTE EXTRA] Criando instâncias dos agentes...")
        
        try:
            barreira = BarreiraSaida("barreira@localhost", "pass")
            print("✅ BarreiraSaida instanciada")
        except Exception as e:
            print(f"❌ Erro ao instanciar BarreiraSaida: {e}")
        
        try:
            vehicle = Vehicle("vehicle@localhost", "pass", "carro", "normal")
            print("✅ Vehicle instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar Vehicle: {e}")
        
        try:
            central = CentralManager("central@localhost", "pass")
            print("✅ CentralManager instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar CentralManager: {e}")
        
        try:
            location = Location("location@localhost", "pass")
            print("✅ Location instanciado")
        except Exception as e:
            print(f"❌ Erro ao instanciar Location: {e}")
        
        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
        print("Verifique se todos os ficheiros estão no lugar correto.")
        return False
    
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_agents())
    sys.exit(0 if success else 1)
