class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class LogFormatter:
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
        style = LogFormatter.AGENT_STYLES.get(agent_type, {
            'color': Colors.WHITE,
            'prefix': 'AGT'
        })
        
        level_colors = {
            'INFO': Colors.BLUE,
            'WARNING': Colors.YELLOW,
            'ERROR': Colors.RED,
            'SUCCESS': Colors.GREEN,
            'DEBUG': Colors.DIM
        }
        
        level_color = level_colors.get(level, Colors.WHITE)
        
        formatted = (
            f"{style['color']}[{style['prefix']}-{agent_id}]{Colors.RESET} "
            f"{level_color}{message}{Colors.RESET}"
        )
        
        return formatted
    
    @staticmethod
    def format_separator(title='', char='─', width=80):
        if title:
            title_formatted = f" {title} "
            padding = (width - len(title_formatted)) // 2
            return f"{Colors.DIM}{char * padding}{title_formatted}{char * padding}{Colors.RESET}"
        return f"{Colors.DIM}{char * width}{Colors.RESET}"
    
    @staticmethod
    def format_header(text):
        return f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{text}{Colors.RESET}"
    
    @staticmethod
    def format_box(lines, title=''):
        max_len = max(len(line) for line in lines) if lines else 0
        width = max(max_len + 4, len(title) + 4)
        
        box = []
        if title:
            box.append(f"{Colors.DIM}╔{'═' * (width - 2)}╗{Colors.RESET}")
            box.append(f"{Colors.DIM}║{Colors.RESET} {Colors.BOLD}{title.center(width - 4)}{Colors.RESET} {Colors.DIM}║{Colors.RESET}")
            box.append(f"{Colors.DIM}╠{'═' * (width - 2)}╣{Colors.RESET}")
        else:
            box.append(f"{Colors.DIM}┌{'─' * (width - 2)}┐{Colors.RESET}")
        
        for line in lines:
            padding = width - len(line) - 4
            box.append(f"{Colors.DIM}│{Colors.RESET} {line}{' ' * padding} {Colors.DIM}│{Colors.RESET}")
        
        box.append(f"{Colors.DIM}╚{'═' * (width - 2)}╝{Colors.RESET}")
        
        return '\n'.join(box)
    
    @staticmethod
    def extract_agent_info(log_line):
        import re
        
        pattern = r'\[(.*?)\s+([^\]]+)\]\s*(.*)'
        match = re.match(pattern, log_line)
        
        if match:
            agent_type = match.group(1).strip()
            agent_id = match.group(2).strip()
            message = match.group(3).strip()
            return agent_type, agent_id, message
        
        pattern2 = r'\[([^\]]+)\]\s*(.*)'
        match2 = re.match(pattern2, log_line)
        
        if match2:
            agent_type = match2.group(1).strip()
            message = match2.group(2).strip()
            return agent_type, 'SYS', message
        
        return None


def print_formatted(agent_type, agent_id, message, level='INFO'):
    print(LogFormatter.format_log(agent_type, agent_id, message, level))


def print_separator(title='', char='─', width=80):
    print(LogFormatter.format_separator(title, char, width))


def print_header(text):
    print(LogFormatter.format_header(text))


def print_box(lines, title=''):
    print(LogFormatter.format_box(lines, title))
