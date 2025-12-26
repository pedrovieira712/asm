import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

async def test_behaviours_syntax():
    """Testa se os behaviours têm sintaxe correta e podem ser instanciados"""
    print("=" * 60)
    print("🔍 TESTE DE SINTAXE DOS BEHAVIOURS")
    print("=" * 60)
    
    errors = []
    
    # Teste 1: Barreira_Saida
    print("\n[1/6] Verificando Barreira_Saida...")
    try:
        from Agents.Barreira_Saida.behaviours.BS_behaviours import (
            ReceberPedidoSaida, VerificarPagamento, 
            ReceberConfirmacaoPagamento, EnviarConfirmacaoSaida
        )
        
        # Tenta criar instâncias
        b1 = ReceberPedidoSaida()
        b2 = VerificarPagamento()
        b3 = ReceberConfirmacaoPagamento()
        b4 = EnviarConfirmacaoSaida()
        
        print(f"  ✅ 4 behaviours OK")
        print(f"     - ReceberPedidoSaida")
        print(f"     - VerificarPagamento")
        print(f"     - ReceberConfirmacaoPagamento")
        print(f"     - EnviarConfirmacaoSaida")
    except Exception as e:
        errors.append(f"Barreira_Saida: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Teste 2: Kiosque_Saida
    print("\n[2/6] Verificando Kiosque_Saida...")
    try:
        from Agents.Kiosque_Saida.Behaviours.Behav_Kiosque_Saida import (
            RecvEntryHourClient, RecvExitRequest, RecvPayment
        )
        
        b1 = RecvEntryHourClient()
        b2 = RecvExitRequest()
        b3 = RecvPayment()
        
        print(f"  ✅ 3 behaviours OK")
        print(f"     - RecvEntryHourClient")
        print(f"     - RecvExitRequest")
        print(f"     - RecvPayment")
    except Exception as e:
        errors.append(f"Kiosque_Saida: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Teste 3: Kiosque_Entrada
    print("\n[3/6] Verificando Kiosque_Entrada...")
    try:
        from Agents.Kiosque_Entrada.Behaviours.Behav_Kiosque_Entrada import (
            RecvEntryRequest, CheckAvailability, ValidateAnnualPass,
            RegisterEntry, SuggestAlternatives, RecvParkInfo,
            SendEntryConfirmation, ProcessAnnualPassPurchase
        )
        
        b1 = RecvEntryRequest()
        b2 = CheckAvailability()
        b3 = ValidateAnnualPass()
        b4 = RegisterEntry()
        b5 = SuggestAlternatives()
        b6 = RecvParkInfo()
        b7 = SendEntryConfirmation()
        b8 = ProcessAnnualPassPurchase()
        
        print(f"  ✅ 8 behaviours OK")
        print(f"     - RecvEntryRequest")
        print(f"     - CheckAvailability")
        print(f"     - ValidateAnnualPass")
        print(f"     - RegisterEntry")
        print(f"     - SuggestAlternatives")
        print(f"     - RecvParkInfo")
        print(f"     - SendEntryConfirmation")
        print(f"     - ProcessAnnualPassPurchase")
    except Exception as e:
        errors.append(f"Kiosque_Entrada: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Teste 4: Vehicle
    print("\n[4/6] Verificando Vehicle...")
    try:
        from Agents.Vehicle.Behaviours.Vc_behav import (
            SendFowardingRequestBehaviour, ReceiveFowardingResponseBehaviour
        )
        
        b1 = SendFowardingRequestBehaviour()
        b2 = ReceiveFowardingResponseBehaviour()
        
        print(f"  ✅ 2 behaviours OK")
        print(f"     - SendFowardingRequestBehaviour")
        print(f"     - ReceiveFowardingResponseBehaviour")
    except Exception as e:
        errors.append(f"Vehicle: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Teste 5: CentralManager
    print("\n[5/6] Verificando CentralManager...")
    try:
        from Agents.CentralManager.Behaviours.Cm_Behav import (
            RecvForwarding, SendParkingSpotRequest, RecvNextParkingSpot,
            SendParkingSpotAproval, RecvParkingSpotAproval, SendUpdateParkingSpotInfo
        )
        
        b1 = RecvForwarding()
        b2 = SendParkingSpotRequest()
        b3 = RecvNextParkingSpot()
        b4 = SendParkingSpotAproval()
        b5 = RecvParkingSpotAproval()
        b6 = SendUpdateParkingSpotInfo()
        
        print(f"  ✅ 6 behaviours OK")
        print(f"     - RecvForwarding")
        print(f"     - SendParkingSpotRequest")
        print(f"     - RecvNextParkingSpot")
        print(f"     - SendParkingSpotAproval")
        print(f"     - RecvParkingSpotAproval")
        print(f"     - SendUpdateParkingSpotInfo")
    except Exception as e:
        errors.append(f"CentralManager: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Teste 6: Location
    print("\n[6/6] Verificando Location...")
    try:
        from Agents.Location.Behaviours.Loc_Behav import (
            RecvRequestsLocation, SendLocationInfo
        )
        
        b1 = RecvRequestsLocation()
        b2 = SendLocationInfo()
        
        print(f"  ✅ 2 behaviours OK")
        print(f"     - RecvRequestsLocation")
        print(f"     - SendLocationInfo")
    except Exception as e:
        errors.append(f"Location: {e}")
        print(f"  ❌ Erro: {e}")
    
    # Resumo
    print("\n" + "=" * 60)
    if len(errors) == 0:
        print("✅ TODOS OS BEHAVIOURS ESTÃO CORRETOS!")
        print("   - Sintaxe válida")
        print("   - Podem ser instanciados")
        print("   - Prontos para uso")
    else:
        print(f"❌ ENCONTRADOS {len(errors)} ERROS:")
        for error in errors:
            print(f"   - {error}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_behaviours_syntax())