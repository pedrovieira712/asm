"""
Formatador de logs para melhorar a visualização do output do sistema multi-agente.
"""

class Colors:
    """Códigos ANSI para cores no terminal"""
    # Cores básicas
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Cores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Cores de fundo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Cores brilhantes
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class LogFormatter:
    """Formatador de logs com cores e ícones para diferentes tipos de agentes"""
    
    # Mapeamento de tipos de agentes para cores e prefixos
    AGENT_STYLES = {
        'Vehicle': {
            'color': Colors.BRIGHT_CYAN,
            'prefix': 'VEH'
        },
        'Park Manager': {
            'color': Colors.BRIGHT_MAGENTA,
            'prefix': 'PMG'
        },
        'Entry Kiosk': {
            'color': Colors.BRIGHT_GREEN,
            'prefix': 'KEN'
        },
        'Exit Kiosk': {
            'color': Colors.BRIGHT_YELLOW,
            'prefix': 'KEX'
        },
        'Barrier Exit': {
            'color': Colors.BRIGHT_RED,
            'prefix': 'BAR'
        },
        'Sensor': {
            'color': Colors.BRIGHT_BLUE,
            'prefix': 'SEN'
        },
        'Central Manager': {
            'color': Colors.BRIGHT_WHITE,
            'prefix': 'CTL'
        },
        'Location': {
            'color': Colors.CYAN,
            'prefix': 'LOC'
        },
        'Wait Zone': {
            'color': Colors.YELLOW,
            'prefix': 'WZN'
        }
    }
    
    @staticmethod
    def format_log(agent_type, agent_id, message, level='INFO'):
        """
        Formata uma mensagem de log com cores e ícones.
        
        Args:
            agent_type: Tipo do agente (Vehicle, Park Manager, etc.)
            agent_id: Identificador do agente (MS-98-NR, P1, etc.)
            message: Mensagem a ser exibida
            level: Nível de log (INFO, WARNING, ERROR, SUCCESS)
        
        Returns:
            String formatada com cores ANSI
        """
        style = LogFormatter.AGENT_STYLES.get(agent_type, {
            'color': Colors.WHITE,
            'prefix': 'AGT'
        })
        
        # Cores por nível de log
        level_colors = {
            'INFO': Colors.BLUE,
            'WARNING': Colors.YELLOW,
            'ERROR': Colors.RED,
            'SUCCESS': Colors.GREEN,
            'DEBUG': Colors.DIM
        }
        
        level_color = level_colors.get(level, Colors.WHITE)
        
        # Formato: [PREFIXO-ID] Mensagem
        formatted = (
            f"{style['color']}[{style['prefix']}-{agent_id}]{Colors.RESET} "
            f"{level_color}{message}{Colors.RESET}"
        )
        
        return formatted
    
    @staticmethod
    def format_separator(title='', char='─', width=80):
        """Cria um separador visual"""
        if title:
            title_formatted = f" {title} "
            padding = (width - len(title_formatted)) // 2
            return f"{Colors.DIM}{char * padding}{title_formatted}{char * padding}{Colors.RESET}"
        return f"{Colors.DIM}{char * width}{Colors.RESET}"
    
    @staticmethod
    def format_header(text):
        """Formata um cabeçalho"""
        return f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{text}{Colors.RESET}"
    
    @staticmethod
    def format_box(lines, title=''):
        """Cria uma caixa ao redor do texto"""
        max_len = max(len(line) for line in lines) if lines else 0
        width = max(max_len + 4, len(title) + 4)
        
        box = []
        # Topo
        if title:
            box.append(f"{Colors.DIM}╔{'═' * (width - 2)}╗{Colors.RESET}")
            box.append(f"{Colors.DIM}║{Colors.RESET} {Colors.BOLD}{title.center(width - 4)}{Colors.RESET} {Colors.DIM}║{Colors.RESET}")
            box.append(f"{Colors.DIM}╠{'═' * (width - 2)}╣{Colors.RESET}")
        else:
            box.append(f"{Colors.DIM}┌{'─' * (width - 2)}┐{Colors.RESET}")
        
        # Conteúdo
        for line in lines:
            padding = width - len(line) - 4
            box.append(f"{Colors.DIM}│{Colors.RESET} {line}{' ' * padding} {Colors.DIM}│{Colors.RESET}")
        
        # Base
        box.append(f"{Colors.DIM}╚{'═' * (width - 2)}╝{Colors.RESET}")
        
        return '\n'.join(box)
    
    @staticmethod
    def extract_agent_info(log_line):
        """
        Extrai informações do agente de uma linha de log existente.
        
        Args:
            log_line: Linha de log original (ex: "[Vehicle MS-98-NR] Message")
        
        Returns:
            Tupla (agent_type, agent_id, message) ou None se não conseguir extrair
        """
        import re
        
        # Padrão: [Tipo ID] Mensagem
        pattern = r'\[(.*?)\s+([^\]]+)\]\s*(.*)'
        match = re.match(pattern, log_line)
        
        if match:
            agent_type = match.group(1).strip()
            agent_id = match.group(2).strip()
            message = match.group(3).strip()
            return agent_type, agent_id, message
        
        # Padrão alternativo: [Tipo] Mensagem (sem ID específico)
        pattern2 = r'\[([^\]]+)\]\s*(.*)'
        match2 = re.match(pattern2, log_line)
        
        if match2:
            agent_type = match2.group(1).strip()
            message = match2.group(2).strip()
            return agent_type, 'SYS', message
        
        return None


def print_formatted(agent_type, agent_id, message, level='INFO'):
    """Helper function para imprimir logs formatados"""
    print(LogFormatter.format_log(agent_type, agent_id, message, level))


def print_separator(title='', char='─', width=80):
    """Helper function para imprimir separadores"""
    print(LogFormatter.format_separator(title, char, width))


def print_header(text):
    """Helper function para imprimir cabeçalhos"""
    print(LogFormatter.format_header(text))


def print_box(lines, title=''):
    """Helper function para imprimir caixas"""
    print(LogFormatter.format_box(lines, title))
