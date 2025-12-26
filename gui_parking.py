import tkinter as tk
from tkinter import ttk, scrolledtext
import asyncio
import threading
from datetime import datetime
from spade.message import Message
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Adicionar path dos agentes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Agents"))

from ManagerParque.managerParque import ManagerParque
from Barreira_Saida.Barreira_saida import BarreiraSaida
from Kiosque_Saida.Kiosque_Saida import Kiosque_saida
from Kiosque_Entrada.Kiosque_Entrada import Kiosque_Entrada
from CentralManager.CentralManager import CentralManager
from Location.Location import Location
from Sensor.sensor import Sensor
from ZonadeEspera.zonadeespera import ZonadeEspera
from Vehicle.Vehicle import Vehicle

# Configuração
from Config import Config as cfg


class ParkingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚗 Sistema de Estacionamento Inteligente")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")
        
        self.agents = {}
        self.vehicle_counter = 1
        self.running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2d2d30", height=60)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header, text="🚗 Sistema de Estacionamento Multi-Agente", 
                        font=("Arial", 18, "bold"), bg="#2d2d30", fg="#ffffff")
        title.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#1e1e1e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel - Status dos Agentes
        left_panel = tk.Frame(main_container, bg="#252526", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        status_label = tk.Label(left_panel, text="📊 Status dos Agentes", 
                               font=("Arial", 14, "bold"), bg="#252526", fg="#ffffff")
        status_label.pack(pady=10)
        
        self.status_text = scrolledtext.ScrolledText(left_panel, height=25, width=45,
                                                     bg="#1e1e1e", fg="#d4d4d4",
                                                     font=("Consolas", 9))
        self.status_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Middle Panel - Controles
        middle_panel = tk.Frame(main_container, bg="#252526", width=350)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        control_label = tk.Label(middle_panel, text="🎮 Controles", 
                                font=("Arial", 14, "bold"), bg="#252526", fg="#ffffff")
        control_label.pack(pady=10)
        
        # Botão Iniciar Sistema
        self.start_button = tk.Button(middle_panel, text="▶️ Iniciar Sistema", 
                                      command=self.start_system,
                                      bg="#0e639c", fg="white", font=("Arial", 12, "bold"),
                                      height=2, width=25, cursor="hand2")
        self.start_button.pack(pady=10)
        
        # Separator
        ttk.Separator(middle_panel, orient='horizontal').pack(fill='x', pady=15)
        
        # Label Cenários
        scenarios_label = tk.Label(middle_panel, text="🎬 Cenários de Teste", 
                                   font=("Arial", 12, "bold"), bg="#252526", fg="#ffffff")
        scenarios_label.pack(pady=10)
        
        # Botões de Cenários
        btn_frame = tk.Frame(middle_panel, bg="#252526")
        btn_frame.pack(pady=5)
        
        self.btn_entrada = tk.Button(btn_frame, text="🚗 Simular Entrada", 
                                     command=self.simulate_entry,
                                     bg="#107c10", fg="white", font=("Arial", 10),
                                     width=20, height=2, state=tk.DISABLED)
        self.btn_entrada.pack(pady=5)
        
        self.btn_saida = tk.Button(btn_frame, text="🚪 Simular Saída", 
                                   command=self.simulate_exit,
                                   bg="#d83b01", fg="white", font=("Arial", 10),
                                   width=20, height=2, state=tk.DISABLED)
        self.btn_saida.pack(pady=5)
        
        self.btn_reencaminhamento = tk.Button(btn_frame, text="🔄 Reencaminhamento", 
                                             command=self.simulate_forwarding,
                                             bg="#0078d4", fg="white", font=("Arial", 10),
                                             width=20, height=2, state=tk.DISABLED)
        self.btn_reencaminhamento.pack(pady=5)
        
        self.btn_pagamento = tk.Button(btn_frame, text="💰 Simular Pagamento", 
                                       command=self.simulate_payment,
                                       bg="#8a3a8c", fg="white", font=("Arial", 10),
                                       width=20, height=2, state=tk.DISABLED)
        self.btn_pagamento.pack(pady=5)
        
        # Info do Parque
        ttk.Separator(middle_panel, orient='horizontal').pack(fill='x', pady=15)
        
        park_info_label = tk.Label(middle_panel, text="🅿️ Info do Parque", 
                                   font=("Arial", 12, "bold"), bg="#252526", fg="#ffffff")
        park_info_label.pack(pady=5)
        
        self.park_info = tk.Label(middle_panel, text="Lugares livres: -\nVeículos: 0", 
                                 font=("Arial", 10), bg="#252526", fg="#d4d4d4",
                                 justify=tk.LEFT)
        self.park_info.pack(pady=5)
        
        # Controles adicionais
        ttk.Separator(middle_panel, orient='horizontal').pack(fill='x', pady=10)
        
        extra_label = tk.Label(middle_panel, text="⚙️ Opções", 
                              font=("Arial", 11, "bold"), bg="#252526", fg="#ffffff")
        extra_label.pack(pady=5)
        
        # Dropdown para tipo de veículo
        type_frame = tk.Frame(middle_panel, bg="#252526")
        type_frame.pack(pady=5)
        
        tk.Label(type_frame, text="Tipo Veículo:", bg="#252526", fg="#d4d4d4",
                font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        self.vehicle_type_var = tk.StringVar(value="carro")
        vehicle_dropdown = ttk.Combobox(type_frame, textvariable=self.vehicle_type_var,
                                       values=["carro", "moto", "camiao", "caravana"],
                                       state="readonly", width=12)
        vehicle_dropdown.pack(side=tk.LEFT)
        
        # Dropdown para tipo de utilizador
        user_frame = tk.Frame(middle_panel, bg="#252526")
        user_frame.pack(pady=5)
        
        tk.Label(user_frame, text="Utilizador:", bg="#252526", fg="#d4d4d4",
                font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        self.user_type_var = tk.StringVar(value="normal")
        user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_type_var,
                                    values=["normal", "grávida", "mobilidade_reduzida", "idoso"],
                                    state="readonly", width=12)
        user_dropdown.pack(side=tk.LEFT)
        
        # Botão para limpar logs
        tk.Button(middle_panel, text="🗑️ Limpar Logs",
                 command=self.clear_logs,
                 bg="#3c3c3c", fg="white", font=("Arial", 9),
                 width=20, height=1).pack(pady=10)
        
        # Right Panel - Logs
        right_panel = tk.Frame(main_container, bg="#252526")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        logs_label = tk.Label(right_panel, text="📝 Logs do Sistema", 
                             font=("Arial", 14, "bold"), bg="#252526", fg="#ffffff")
        logs_label.pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(right_panel, height=35,
                                                  bg="#1e1e1e", fg="#d4d4d4",
                                                  font=("Consolas", 9))
        self.log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Tags para cores nos logs
        self.log_text.tag_config("SUCCESS", foreground="#4ec9b0")
        self.log_text.tag_config("ERROR", foreground="#f48771")
        self.log_text.tag_config("INFO", foreground="#569cd6")
        self.log_text.tag_config("WARNING", foreground="#dcdcaa")
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] ", level)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
        self.log("🗑️ Logs limpos", "INFO")
        
    def update_status(self):
        self.status_text.delete(1.0, tk.END)
        
        status = "═══════════════════════════════\n"
        status += "        AGENTES ATIVOS\n"
        status += "═══════════════════════════════\n\n"
        
        if self.agents:
            status += f"✅ ManagerParque\n"
            status += f"✅ BarreiraSaida\n"
            status += f"✅ KiosqueSaida\n"
            status += f"✅ KiosqueEntrada\n"
            status += f"✅ CentralManager\n"
            status += f"✅ Location\n"
            status += f"✅ Sensor Lugar\n"
            status += f"✅ Sensor Saída\n"
            status += f"✅ ZonadeEspera\n"
            
            if 'vehicle1' in self.agents:
                status += f"🚗 Vehicle 1\n"
        else:
            status += "❌ Sistema não iniciado\n"
            
        self.status_text.insert(tk.END, status)
        
    def start_system(self):
        self.log("🚀 Iniciando sistema...", "INFO")
        self.start_button.config(state=tk.DISABLED, text="⏳ Iniciando...")
        
        # Executar em thread separada
        thread = threading.Thread(target=self._start_agents_thread)
        thread.daemon = True
        thread.start()
        
    def _start_agents_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._start_agents())
        
    async def _start_agents(self):
        try:
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
            PASSWORD = cfg.get_password()
            
            self.log("Criando ManagerParque...", "INFO")
            manager = ManagerParque(JIDS["manager_parque"], PASSWORD, "P1", capacity=50, max_height=2.5)
            await manager.start()
            self.agents["manager_parque"] = manager
            
            self.log("Criando BarreiraSaida...", "INFO")
            barreira = BarreiraSaida(JIDS["barreira_saida"], PASSWORD)
            barreira.manager_jid = JIDS["manager_parque"]
            barreira.sensor_jid = JIDS["sensor_saida"]
            await barreira.start()
            self.agents["barreira_saida"] = barreira
            
            self.log("Criando KiosqueSaida...", "INFO")
            kiosque_saida = Kiosque_saida(JIDS["kiosque_saida"], PASSWORD)
            kiosque_saida.manager_jid = JIDS["manager_parque"]
            await kiosque_saida.start()
            self.agents["kiosque_saida"] = kiosque_saida
            
            self.log("Criando KiosqueEntrada...", "INFO")
            kiosque_entrada = Kiosque_Entrada(JIDS["kiosque_entrada"], PASSWORD, "P1")
            kiosque_entrada.manager_jid = JIDS["manager_parque"]
            kiosque_entrada.quiosque_saida_jid = JIDS["kiosque_saida"]
            kiosque_entrada.central_manager_jid = JIDS["central_manager"]
            await kiosque_entrada.start()
            self.agents["kiosque_entrada"] = kiosque_entrada
            
            self.log("Criando CentralManager...", "INFO")
            central = CentralManager(JIDS["central_manager"], PASSWORD)
            central.location_jid = JIDS["location"]
            await central.start()
            self.agents["central_manager"] = central
            
            self.log("Criando Location...", "INFO")
            location = Location(JIDS["location"], PASSWORD)
            location.park_locations = {JIDS["manager_parque"]: {"nome": "Parque 1", "distancia": 0}}
            await location.start()
            self.agents["location"] = location
            
            self.log("Criando Sensores...", "INFO")
            sensor_lugar = Sensor(JIDS["sensor_lugar1"], PASSWORD, "LUGAR", "L1")
            await sensor_lugar.start()
            self.agents["sensor_lugar1"] = sensor_lugar
            
            sensor_saida = Sensor(JIDS["sensor_saida"], PASSWORD, "SAIDA")
            await sensor_saida.start()
            self.agents["sensor_saida"] = sensor_saida
            
            self.log("Criando ZonadeEspera...", "INFO")
            zona = ZonadeEspera(JIDS["zona_espera"], PASSWORD)
            await zona.start()
            self.agents["zona_espera"] = zona
            
            self.log("✅ Sistema iniciado com sucesso!", "SUCCESS")
            self.running = True
            
            # Atualizar UI
            self.root.after(0, self._enable_buttons)
            self.root.after(0, self.update_status)
            self.root.after(0, self._update_park_info)
            
        except Exception as e:
            self.log(f"❌ Erro ao iniciar: {str(e)}", "ERROR")
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL, text="▶️ Iniciar Sistema"))
            
    def _enable_buttons(self):
        self.btn_entrada.config(state=tk.NORMAL)
        self.btn_saida.config(state=tk.NORMAL)
        self.btn_reencaminhamento.config(state=tk.NORMAL)
        self.btn_pagamento.config(state=tk.NORMAL)
        self.start_button.config(text="✅ Sistema Ativo")
        
    def _update_park_info(self):
        if "manager_parque" in self.agents:
            manager = self.agents["manager_parque"]
            livres = manager.get_free_spots()
            ocupados = manager.occupied_spots
            total = manager.capacity
            
            info = f"Capacidade: {total}\n"
            info += f"Lugares livres: {livres}\n"
            info += f"Lugares ocupados: {ocupados}\n"
            info += f"Veículos criados: {self.vehicle_counter - 1}"
            
            self.park_info.config(text=info)
            
    def simulate_entry(self):
        self.log("🚗 Simulando entrada de veículo...", "WARNING")
        thread = threading.Thread(target=self._simulate_entry_thread)
        thread.daemon = True
        thread.start()
        
    def _simulate_entry_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._simulate_entry_async())
        
    async def _simulate_entry_async(self):
        try:
            jid = f"vehicle{self.vehicle_counter}@localhost"
            
            # Obter tipos selecionados
            vehicle_type = self.vehicle_type_var.get()
            user_type = self.user_type_var.get()
            
            self.log(f"Criando veículo: {jid}", "INFO")
            self.log(f"🚙 Tipo: {vehicle_type} | 👤 Utilizador: {user_type}", "INFO")
            
            vehicle = Vehicle(jid, "password123", vehicle_type=vehicle_type, user_type=user_type)
            vehicle.central_manager_jid = "central_manager@localhost"
            await vehicle.start()
            
            self.agents[f"vehicle{self.vehicle_counter}"] = vehicle
            vehicle_num = self.vehicle_counter
            self.vehicle_counter += 1
            
            # Aguardar veículo iniciar
            await asyncio.sleep(1)
            
            # Definir altura baseada no tipo de veículo
            alturas = {
                "carro": 1.5,
                "moto": 1.0,
                "camiao": 3.5,
                "caravana": 2.8
            }
            altura = alturas.get(vehicle_type, 1.5)
            
            # Enviar pedido de entrada ao Kiosque
            msg = Message(to="kiosque_entrada@localhost")
            msg.metadata["tipo"] = "PEDIDO_ENTRADA"
            msg.body = str({
                "id_veiculo": jid,
                "tipo": vehicle_type,
                "altura": altura,
                "user_type": user_type,
                "plate": f"AA-{vehicle_num:02d}-BB"
            })
            
            # Enviar mensagem
            from spade.behaviour import OneShotBehaviour
            class SendEntry(OneShotBehaviour):
                async def run(self):
                    await self.send(msg)
            
            vehicle.add_behaviour(SendEntry())
            
            self.log(f"✅ Veículo {jid} criado e pedido de entrada enviado ao Kiosque", "SUCCESS")
            self.log(f"📝 Matrícula: AA-{vehicle_num:02d}-BB | Altura: {altura}m", "INFO")
            self.root.after(0, self.update_status)
            self.root.after(0, self._update_park_info)
            
        except Exception as e:
            self.log(f"❌ Erro na entrada: {str(e)}", "ERROR")
            
    def simulate_exit(self):
        self.log("🚪 Simulando saída de veículo...", "WARNING")
        thread = threading.Thread(target=self._simulate_exit_thread)
        thread.daemon = True
        thread.start()
        
    def _simulate_exit_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._simulate_exit_async())
        
    async def _simulate_exit_async(self):
        try:
            # Verificar se existe veículo para sair
            vehicle_keys = [k for k in self.agents.keys() if k.startswith("vehicle")]
            if not vehicle_keys:
                self.log("⚠️  Nenhum veículo no parque para sair", "WARNING")
                return
            
            # Pegar primeiro veículo
            vehicle_key = vehicle_keys[0]
            vehicle = self.agents[vehicle_key]
            vehicle_jid = str(vehicle.jid)
            
            self.log(f"🚗 Veículo {vehicle_jid} vai solicitar saída", "INFO")
            
            # Enviar pedido de saída à Barreira
            msg = Message(to="barreira_saida@localhost")
            msg.metadata["tipo"] = "PEDIDO_SAIDA"
            msg.body = str({
                "id_veiculo": vehicle_jid,
                "matricula": vehicle_jid.split("@")[0]
            })
            
            from spade.behaviour import OneShotBehaviour
            class SendExit(OneShotBehaviour):
                async def run(self):
                    await self.send(msg)
            
            vehicle.add_behaviour(SendExit())
            
            self.log(f"✅ Pedido de saída enviado para {vehicle_jid}", "SUCCESS")
            self.log(f"📍 Barreira vai verificar pagamento com Manager", "INFO")
            
        except Exception as e:
            self.log(f"❌ Erro na saída: {str(e)}", "ERROR")
        
    def simulate_forwarding(self):
        self.log("🔄 Simulando reencaminhamento...", "WARNING")
        thread = threading.Thread(target=self._simulate_forwarding_thread)
        thread.daemon = True
        thread.start()
        
    def _simulate_forwarding_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._simulate_forwarding_async())
        
    async def _simulate_forwarding_async(self):
        try:
            jid = f"vehicle{self.vehicle_counter}@localhost"
            self.log(f"Criando veículo para reencaminhamento: {jid}", "INFO")
            
            vehicle = Vehicle(jid, "password123", vehicle_type="carro", user_type="normal")
            vehicle.central_manager_jid = "central_manager@localhost"
            await vehicle.start()
            
            self.agents[f"vehicle{self.vehicle_counter}"] = vehicle
            self.vehicle_counter += 1
            
            self.log(f"✅ Veículo {jid} enviou pedido de reencaminhamento", "SUCCESS")
            self.root.after(0, self.update_status)
            self.root.after(0, self._update_park_info)
            
        except Exception as e:
            self.log(f"❌ Erro no reencaminhamento: {str(e)}", "ERROR")
            
    def simulate_payment(self):
        self.log("💰 Simulando pagamento...", "WARNING")
        thread = threading.Thread(target=self._simulate_payment_thread)
        thread.daemon = True
        thread.start()
        
    def _simulate_payment_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._simulate_payment_async())
        
    async def _simulate_payment_async(self):
        try:
            from datetime import datetime, timedelta
            
            # Verificar se existe veículo
            vehicle_keys = [k for k in self.agents.keys() if k.startswith("vehicle")]
            if not vehicle_keys:
                self.log("⚠️  Nenhum veículo para pagar", "WARNING")
                return
            
            # Pegar primeiro veículo
            vehicle_key = vehicle_keys[0]
            vehicle = self.agents[vehicle_key]
            vehicle_jid = str(vehicle.jid)
            matricula = vehicle_jid.split("@")[0]
            
            self.log(f"💳 Veículo {vehicle_jid} vai ao Kiosque de Saída", "INFO")
            
            # 1. Primeiro solicitar hora de entrada ao Kiosque Saída
            msg1 = Message(to="kiosque_saida@localhost")
            msg1.metadata["tipo"] = "PEDIDO_SAIDA_KIOSQUE"
            msg1.body = matricula
            
            from spade.behaviour import OneShotBehaviour
            class RequestExit(OneShotBehaviour):
                async def run(self):
                    await self.send(msg1)
            
            vehicle.add_behaviour(RequestExit())
            
            self.log(f"📋 Solicitando cálculo de pagamento para {matricula}", "INFO")
            
            # Aguardar um pouco
            await asyncio.sleep(2)
            
            # 2. Simular que recebeu valor e vai pagar
            # Calcular tempo fictício (30 minutos = 1.50€)
            tempo_minutos = 30
            valor = tempo_minutos * 0.05
            
            self.log(f"💵 Tempo: {tempo_minutos} min → Valor: {valor:.2f}€", "INFO")
            
            # 3. Enviar pagamento
            msg2 = Message(to="kiosque_saida@localhost")
            msg2.metadata["tipo"] = "PAGAMENTO"
            msg2.body = str({
                "matricula": matricula,
                "valor_pago": valor,
                "hora_pagamento": datetime.now().isoformat()
            })
            
            class SendPayment(OneShotBehaviour):
                async def run(self):
                    await self.send(msg2)
            
            vehicle.add_behaviour(SendPayment())
            
            self.log(f"✅ Pagamento de {valor:.2f}€ enviado por {matricula}", "SUCCESS")
            self.log(f"📤 Kiosque vai notificar Manager sobre pagamento", "INFO")
            
        except Exception as e:
            self.log(f"❌ Erro no pagamento: {str(e)}", "ERROR")
        
    def run(self):
        self.log("🎯 Interface gráfica iniciada", "SUCCESS")
        self.log("ℹ️  Pressiona 'Iniciar Sistema' para começar", "INFO")
        self.update_status()
        self.root.mainloop()


if __name__ == "__main__":
    gui = ParkingGUI()
    gui.run()
