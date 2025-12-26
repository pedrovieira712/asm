# ManagerParque/__init__.py
from spade.agent import Agent
from ManagerParque.Behaviours.Mp_behav import *

class ManagerParque(Agent):
    def __init__(self, jid, password, park_id, capacity, max_height=None):
        super().__init__(jid, password)

        self.park_id = park_id
        self.capacity = capacity
        self.max_height = max_height

        # Lista de lugares (podes adaptar a estrutura)
        self.parking_spots = []      # cada lugar: {"id": 1, "ocupado": False, ...}
        self.occupied_spots = 0

        # Pagamentos registados por veículo
        #   ex: {"AA-00-BB": {"pago": True, "hora_pagamento": datetime_obj}}
        self.payments = {}

        # Multas associadas ao veículo
        self.fines = {}              # ex: {"AA-00-BB": [lista_de_multas]}

        # Características que o parque suporta (para reencaminhamento)
        #   ex: tipos de veículo, altura máxima, etc.
        self.supported_vehicle_types = ["carro", "moto"]
        self.supports_electric = True

    def print(self, txt):
        print(f"[MANAGER_PARQUE {self.park_id}] {txt}")

    async def setup(self):
        self.print(f"ManagerParque [{self.park_id}] iniciado")

        # 1) Entrada (disponível / não disponível) – quiosque de entrada
        self.add_behaviour(VerificarEntradaKiosque())

        # 2) Saída + multa – barreira de saída
        self.add_behaviour(ProcessarSaidaBarreira())

        # 3) Reencaminhamento – pedidos do Manager Central
        self.add_behaviour(ResponderReencaminhamentoCentral())

    # ---------- Helpers simples ----------

    def get_free_spots(self):
        return self.capacity - self.occupied_spots

    def has_free_spot_for(self, vehicle_info: dict) -> bool:
        """
        Verifica se existe lugar disponível que corresponda
        às características do veículo (altura, tipo, elétrico, etc.).
        Aqui podes pôr a tua lógica real.
        """
        if self.get_free_spots() <= 0:
            return False

        # Exemplos de verificações
        v_type = vehicle_info.get("tipo")
        v_height = vehicle_info.get("altura")
        is_electric = vehicle_info.get("eletrico", False)

        if v_type and v_type not in self.supported_vehicle_types:
            return False

        if self.max_height is not None and v_height is not None:
            if v_height > self.max_height:
                return False

        if is_electric and not self.supports_electric:
            return False

        return True

    def is_payment_valid(self, vehicle_id, now, max_delay_minutes=15):
        """
        Verifica se o veículo pagou e se ainda está dentro dos 15 minutos.
        Devolve (pago, fora_de_tempo)
        """
        info = self.payments.get(vehicle_id)
        if not info or not info.get("pago"):
            return False, False

        hora_pagamento = info.get("hora_pagamento")
        if hora_pagamento is None:
            return True, False

        delta = now - hora_pagamento
        fora_de_tempo = delta.total_seconds() > max_delay_minutes * 60
        return True, fora_de_tempo

    def add_fine(self, vehicle_id, motivo):
        self.fines.setdefault(vehicle_id, []).append(motivo)
