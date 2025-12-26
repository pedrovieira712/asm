"""
Utilitários para prints coloridos no terminal
Inspirado em: https://github.com/Katilho/Trabalho-ASM-2023-2024
"""


class Colors:
    """Cores ANSI para terminal"""
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    DARK_BLUE = '\033[34m'


def print_c(text, color="black"):
    """Print colorido no terminal"""
    color_map = {
        "black": Colors.BLACK,
        "red": Colors.RED,
        "green": Colors.GREEN,
        "yellow": Colors.YELLOW,
        "blue": Colors.BLUE,
        "magenta": Colors.MAGENTA,
        "cyan": Colors.CYAN,
        "white": Colors.WHITE,
        "bright_red": Colors.BRIGHT_RED,
        "bright_green": Colors.BRIGHT_GREEN,
        "bright_yellow": Colors.BRIGHT_YELLOW,
        "bright_blue": Colors.BRIGHT_BLUE,
        "bright_magenta": Colors.BRIGHT_MAGENTA,
        "bright_cyan": Colors.BRIGHT_CYAN,
        "dark blue": Colors.DARK_BLUE,
    }
    
    color_code = color_map.get(color.lower(), Colors.RESET)
    print(f"{color_code}{text}{Colors.RESET}")


def print_error(text):
    """Print de erro (vermelho)"""
    print_c(f"❌ ERROR: {text}", "red")


def print_warning(text):
    """Print de aviso (amarelo)"""
    print_c(f"⚠️  WARNING: {text}", "yellow")


def print_success(text):
    """Print de sucesso (verde)"""
    print_c(f"✅ SUCCESS: {text}", "green")


def print_info(text):
    """Print informativo (azul)"""
    print_c(f"ℹ️  INFO: {text}", "blue")
