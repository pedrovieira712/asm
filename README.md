<img src='https://www.uminho.pt/PT/ensino/Cursos/PublishingImages/engenharia-informatica-m.png' width="30%"/>

<h3 align="center">Mestrado em Engenharia Informática <br> Perfil de Sistemas Inteligentes <br> Trabalho prático de Agentes e Sistemas Multiagente <br> 2024/2025 </h3>

---

## 🚗 Sistema de Estacionamento Inteligente Multi-Agente

Sistema desenvolvido usando o framework SPADE para simular a gestão inteligente de um parque de estacionamento com múltiplos agentes autónomos.

---

## 📋 Estrutura do Projeto

```
asm/
├── Agents/                    # Agentes do sistema
│   ├── ManagerParque/        # Gestão do parque
│   ├── Barreira_Saida/       # Controlo de saídas
│   ├── Kiosque_Saida/        # Pagamentos na saída
│   ├── Kiosque_Entrada/      # Validação de entradas
│   ├── CentralManager/       # Coordenação central
│   ├── Location/             # Serviço de localização
│   ├── Sensor/               # Sensores de ocupação
│   ├── ZonadeEspera/         # Gestão de fila de espera
│   └── Vehicle/              # Veículos
├── Utils/                    # Utilitários
│   └── Prints.py            # Funções de print colorido
├── resources/               # Recursos auxiliares
│   ├── stats.json          # Estatísticas
│   └── logs.txt            # Logs do sistema
├── Config.py               # Configuração central (JIDs, domínio)
├── stats.py                # Módulo de estatísticas
├── main.py                 # Script principal (terminal)
├── gui_parking.py          # Interface gráfica
└── .env                    # Variáveis de ambiente
```

---

## 🎯 Agentes do Sistema

### 1. **ManagerParque**
- Gere lugares disponíveis no parque
- Valida entradas/saídas
- Mantém registo de pagamentos e multas
- Responde a pedidos de reencaminhamento

### 2. **Barreira de Saída**
- Recebe pedidos de saída dos veículos
- Verifica pagamento com Manager
- Controla abertura/fecho da barreira
- Notifica sensores

### 3. **Kiosque de Saída**
- Calcula valor a pagar (€0.05/min)
- Processa pagamentos
- Aplica multas se necessário
- Notifica Manager

### 4. **Kiosque de Entrada**
- Valida pedidos de entrada
- Verifica disponibilidade com Manager
- Valida passes anuais
- Regista hora de entrada

### 5. **CentralManager**
- Coordena reencaminhamento entre parques
- Solicita parques alternativos ao Location
- Verifica disponibilidade noutros parques

### 6. **Location**
- Fornece informação sobre parques próximos
- Mantém mapa de localização dos parques

### 7. **Zona de Espera**
- Gere fila de veículos em espera
- Fornece veículos quando há disponibilidade

### 8. **Sensores**
- Detectam ocupação de lugares
- Atualizam estado (LIVRE/RESERVADO/OCUPADO)

### 9. **Vehicle**
- Representa veículos no sistema
- Envia pedidos de entrada/saída/reencaminhamento

---

## 📡 Comunicação entre Agentes

### Cenário 1: Entrada Disponível
```
Vehicle → Kiosque_Entrada : PEDIDO_ENTRADA
Kiosque_Entrada → ManagerParque : ENTRADA_VERIFICAR
ManagerParque → Sensor : LUGAR_LIVRE
ManagerParque → Kiosque_Entrada : PODE_ENTRAR
Kiosque_Entrada → Kiosque_Saida : HORA_ENTRADA
```

### Cenário 2: Saída com Pagamento
```
Vehicle → Barreira_Saida : PEDIDO_SAIDA
Barreira_Saida → ManagerParque : PEDIDO_SAIR
Vehicle → Kiosque_Saida : PEDIDO_SAIDA_KIOSQUE
Kiosque_Saida → Vehicle : VALOR_A_PAGAR
Vehicle → Kiosque_Saida : PAGAMENTO
Kiosque_Saida → ManagerParque : CONFIRMACAO_PAGAMENTO
ManagerParque → Barreira_Saida : ABRIR_BARREIRA
Barreira_Saida → Sensor : SENSOR_LIVRE
```

### Cenário 3: Reencaminhamento
```
Vehicle → CentralManager : REENCAMINHAMENTO
CentralManager → Location : PARQUE_PROXIMO
Location → CentralManager : PARQUE
CentralManager → ManagerParque : VERIFICAR_LUGAR
ManagerParque → CentralManager : RESPOSTA_VERIFICAR_LUGAR
CentralManager → Vehicle : PARQUE_ALTERNATIVO
```

---

## 🚀 Como Executar

### Pré-requisitos
```bash
conda create -n sma python=3.11
conda activate sma
pip install spade python-dotenv
```

### Configurar Openfire
1. Instalar Openfire Server
2. Criar utilizadores:
   - manager_parque
   - barreira_saida
   - kiosque_saida
   - kiosque_entrada
   - central_manager
   - location
   - sensor_lugar1
   - sensor_saida
   - zona_espera
   - vehicle1, vehicle2, ...
3. Password: `password123`

### Executar Terminal
```bash
python main.py
```

### Executar Interface Gráfica
```bash
python gui_parking.py
```

---

## 🎮 Interface Gráfica

### Funcionalidades
- ✅ Visualização em tempo real dos agentes
- ✅ Simulação de entrada de veículos
- ✅ Simulação de saída
- ✅ Simulação de pagamento
- ✅ Reencaminhamento entre parques
- ✅ Logs coloridos
- ✅ Estatísticas do parque
- ✅ Seleção de tipo de veículo (carro/moto/camião/caravana)
- ✅ Seleção de tipo de utilizador (normal/grávida/mobilidade_reduzida/idoso)

---

## 📊 Estatísticas

O sistema gera estatísticas em `resources/stats.json`:
- Total de entradas
- Total de saídas
- Veículos dentro do parque
- Duração média de permanência
- Receita total

---

## 🔧 Configuração

Editar `.env`:
```env
DOMAIN=localhost
PASSWORD=password123
```

---

## 📝 Keywords

ASM, Agentes e Sistemas Multiagente, SPADE, Multi-Agent Systems, Parking Management, Smart Parking, XMPP, UMinho, MIEI, Engenharia Informática

---

## 🙏 Inspiração

Estrutura baseada no trabalho: [Katilho/Trabalho-ASM-2023-2024](https://github.com/Katilho/Trabalho-ASM-2023-2024)
