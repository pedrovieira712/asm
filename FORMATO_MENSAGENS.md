# Formato de Mensagens ACL com JsonPickle

## Padrão Utilizado (baseado em Katilho/Trabalho-ASM-2023-2024)

### Estrutura das Mensagens

```python
from spade.message import Message
import jsonpickle

# ENVIAR MENSAGEM
msg = Message(
    to="destinatario@localhost",
    metadata={"performative": "request"},  # ou "inform", "confirm"
    body=jsonpickle.encode(dados)  # Serializar objeto/dict/string
)
await self.send(msg)

# RECEBER MENSAGEM
msg = await self.receive(timeout=1)
if msg:
    performative = msg.metadata.get("performative")
    dados = jsonpickle.decode(msg.body)  # Deserializar
```

## Performatives ACL (FIPA)

### **request** - Pedido
- Quando um agente pede algo a outro
- Exemplos:
  - Veículo → Barreira: pedido de saída
  - Veículo → Kiosque Entrada: pedido de entrada
  - Kiosque → Manager: verificação de disponibilidade

### **inform** - Informação
- Quando um agente informa/notifica outro
- Exemplos:
  - Barreira → Sensor: notificar saída
  - Kiosque Entrada → Kiosque Saída: enviar hora de entrada
  - Manager → qualquer: enviar informação

### **confirm** - Confirmação
- Quando um agente confirma uma ação/pedido
- Exemplos:
  - Manager → Kiosque: confirmar entrada autorizada
  - Barreira → Veículo: confirmar barreira aberta

## Alterações Feitas

### ✅ Barreira_Saida (BS_behaviours.py)
**Antes:**
```python
msg.metadata["tipo"] = "PEDIDO_SAIDA"
msg.body = string
```
**Agora:**
```python
metadata={"performative": "request"}
body=jsonpickle.encode(id_veiculo)
```

### ✅ Kiosque_Entrada (Behav_Kiosque_Entrada.py)
**Antes:**
```python
msg.metadata["tipo"] = "PEDIDO_ENTRADA"
dados = eval(msg.body)
```
**Agora:**
```python
metadata={"performative": "request"}
dados = jsonpickle.decode(msg.body)
```

### ✅ Kiosque_Saida (Behav_Kiosque_Saida.py)
**Antes:**
```python
msg.metadata["tipo"] = "HORA_ENTRADA"
msg.body = str(dict)
```
**Agora:**
```python
metadata={"performative": "inform"}
body=jsonpickle.encode(entrada_data)
```

### 🔄 Pendentes de Ajustar
1. **CentralManager** (Cm_Behav.py)
   - RecvForwarding: `"tipo": "REENCAMINHAMENTO"` → `"performative": "request"`
   - SendParkingSpotRequest: usar jsonpickle
   - RecvNextParkingSpot: `"tipo": "PARQUE"` → `"performative": "inform"`

2. **Location** (Loc_Behav.py)
   - RecvRequestsLocation: ajustar para performatives
   - SendLocationInfo: usar jsonpickle.encode()

3. **ManagerParque** (Mp_behav.py)
   - Todos os behaviours precisam ser ajustados

4. **Sensor** (Sensor_Behav.py)
   - AtualizarEstadoSensor: ajustar recebimento de mensagens

5. **Vehicle** (Vc_behav.py)
   - SendFowardingRequestBehaviour: usar performative="request"
   - ReceiveFowardingResponseBehaviour: usar jsonpickle.decode()

6. **GUI e Main**: Atualizar chamadas para usar jsonpickle

## Exemplo Completo de Comunicação

### Cenário: Entrada de Veículo

```python
# 1. Vehicle → Kiosque_Entrada (REQUEST)
dados_veiculo = {
    "id_veiculo": "vehicle1@localhost",
    "tipo": "carro",
    "altura": 1.5,
    "user_type": "normal"
}
msg = Message(
    to="kiosque_entrada@localhost",
    metadata={"performative": "request"},
    body=jsonpickle.encode(dados_veiculo)
)

# 2. Kiosque_Entrada → ManagerParque (REQUEST)
msg = Message(
    to="manager_parque@localhost",
    metadata={"performative": "request"},
    body=jsonpickle.encode(dados_veiculo)
)

# 3. ManagerParque → Kiosque_Entrada (CONFIRM)
msg = Message(
    to="kiosque_entrada@localhost",
    metadata={"performative": "confirm"},
    body=jsonpickle.encode("PODE_ENTRAR")
)

# 4. Kiosque_Entrada → Vehicle (CONFIRM)
msg = Message(
    to="vehicle1@localhost",
    metadata={"performative": "confirm"},
    body=jsonpickle.encode("ENTRADA_APROVADA")
)

# 5. Kiosque_Entrada → Kiosque_Saida (INFORM)
entrada_data = {
    "id_veiculo": "vehicle1@localhost",
    "hora_entrada": "2025-12-26T10:30:00"
}
msg = Message(
    to="kiosque_saida@localhost",
    metadata={"performative": "inform"},
    body=jsonpickle.encode(entrada_data)
)
```

## Referência do GitHub do Ano Passado

```python
# Exemplo de Airport enviando a Hangar
msg = Message(
    to=hangar_name, 
    body=jsonpickle.encode(trip), 
    metadata={"performative": "request"}
)

# Exemplo de CT enviando a Plane
msg = Message(
    to=plane_jid, 
    metadata={"performative": "inform"}, 
    body=jsonpickle.encode(msg_body)
)

# Exemplo de Plane confirmando aterragem
msg = Message(
    to=ct_destin, 
    metadata={"performative": "confirm"}, 
    body=jsonpickle.encode(self.agent.jid)
)
```

## Benefícios

1. **Padrão FIPA ACL** - Standard de comunicação entre agentes
2. **Serialização robusta** - jsonpickle suporta objetos complexos
3. **Compatibilidade** - Alinhado com trabalho académico anterior
4. **Clareza semântica** - Performatives descrevem tipo de interação
5. **Type safety** - jsonpickle preserva tipos de dados

## Próximos Passos

1. Ajustar CentralManager, Location, ManagerParque, Sensor, Vehicle
2. Atualizar GUI para usar novo formato (gui_parking.py)
3. Atualizar main.py se necessário
4. Testar comunicação entre todos os agentes
5. Fazer commit das alterações

