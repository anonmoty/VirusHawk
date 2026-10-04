from datetime import datetime
from colorama import Fore, Style

class Log:
    def _t(self): return datetime.now().strftime("%H:%M:%S")
    def info(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.CYAN + " [i] " + Fore.WHITE + m)
    def ok(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.GREEN + " [✓] " + Fore.WHITE + m)
    def warn(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.YELLOW + " [!] " + Fore.WHITE + m)
    def err(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.RED + " [✗] " + Fore.WHITE + m)
    def threat(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.RED + Style.BRIGHT + " [💀] " + Fore.LIGHTRED_EX + m)
    def clean(self, m): print("  " + Fore.LIGHTBLACK_EX + "[" + self._t() + "]" + Fore.GREEN + " [✅] " + Fore.GREEN + m)
