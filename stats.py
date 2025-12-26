"""
Módulo de estatísticas do sistema de estacionamento
Inspirado em: https://github.com/Katilho/Trabalho-ASM-2023-2024
"""
import json
from datetime import datetime
from Config import Config as cfg


def add_vehicle_entry(vehicle_id, entry_time, vehicle_type="carro", user_type="normal"):
    """Adiciona entrada de veículo às estatísticas"""
    stats_file = cfg.stats_file_name()
    
    try:
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = []
    
    entry = {
        "vehicle_id": vehicle_id,
        "entry_time": entry_time,
        "vehicle_type": vehicle_type,
        "user_type": user_type,
        "exit_time": None,
        "duration_minutes": None,
        "payment": None
    }
    
    stats.append(entry)
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4)


def add_vehicle_exit(vehicle_id, exit_time, payment_value):
    """Adiciona saída de veículo às estatísticas"""
    stats_file = cfg.stats_file_name()
    
    try:
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    # Encontrar entrada do veículo
    for entry in stats:
        if entry["vehicle_id"] == vehicle_id and entry["exit_time"] is None:
            entry["exit_time"] = exit_time
            entry["payment"] = payment_value
            
            # Calcular duração
            entry_dt = datetime.fromisoformat(entry["entry_time"])
            exit_dt = datetime.fromisoformat(exit_time)
            duration = (exit_dt - entry_dt).total_seconds() / 60
            entry["duration_minutes"] = round(duration, 2)
            break
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4)


def get_statistics():
    """Retorna estatísticas agregadas"""
    stats_file = cfg.stats_file_name()
    
    try:
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "total_entries": 0,
            "total_exits": 0,
            "vehicles_inside": 0,
            "average_duration": 0,
            "total_revenue": 0
        }
    
    total_entries = len(stats)
    completed_visits = [s for s in stats if s["exit_time"] is not None]
    total_exits = len(completed_visits)
    vehicles_inside = total_entries - total_exits
    
    if completed_visits:
        avg_duration = sum(s["duration_minutes"] for s in completed_visits) / len(completed_visits)
        total_revenue = sum(s["payment"] for s in completed_visits if s["payment"])
    else:
        avg_duration = 0
        total_revenue = 0
    
    return {
        "total_entries": total_entries,
        "total_exits": total_exits,
        "vehicles_inside": vehicles_inside,
        "average_duration": round(avg_duration, 2),
        "total_revenue": round(total_revenue, 2)
    }


def write_stats_summary(output_file):
    """Escreve resumo das estatísticas"""
    stats = get_statistics()
    
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=4)
    
    return stats
