import sys, time, random, shutil
from colorama import Fore, Back, Style, init
init(autoreset=True)

class Anim:
    @staticmethod
    def _w():
        try: return shutil.get_terminal_size().columns
        except: return 80

    @classmethod
    def matrix(cls, dur=1.0):
        w = min(cls._w(), 85)
        chars = "01アイウエオカキクケコ"
        end = time.time() + dur
        while time.time() < end:
            line = ""
            for _ in range(w):
                r = random.random()
                if r < 0.08: line += Fore.LIGHTGREEN_EX + random.choice(chars)
                elif r < 0.12: line += Fore.GREEN + random.choice("01")
                else: line += " "
            print(line + Style.RESET_ALL)
            time.sleep(0.02)

    @classmethod
    def glitch(cls, text, n=2):
        g = "▓▒░█▄▀■□╳"
        for _ in range(n):
            out = ""
            for ch in text:
                if ch != " " and random.random() < 0.15:
                    out += random.choice([Fore.RED, Fore.CYAN]) + random.choice(g)
                else:
                    out += Fore.LIGHTRED_EX + ch
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write("\r" + Fore.LIGHTRED_EX + text + Style.RESET_ALL + "\n")

    @classmethod
    def typing(cls, text, speed=0.02, color=Fore.GREEN):
        for ch in text:
            sys.stdout.write(color + ch)
            sys.stdout.flush()
            time.sleep(speed)
        print(Style.RESET_ALL)

    @classmethod
    def scan_line(cls, module, status, icon="🔍"):
        hx = ''.join(random.choices("0123456789abcdef", k=8))
        sys.stdout.write(
            "\r  " + Fore.LIGHTBLACK_EX + "[" + time.strftime("%H:%M:%S") + "] " +
            icon + " " + Fore.WHITE + module.ljust(22) +
            Fore.LIGHTBLACK_EX + " 0x" + hx + " " + status + Style.RESET_ALL + "\n"
        )
        sys.stdout.flush()

    @classmethod
    def progress(cls, cur, total, desc=""):
        if total == 0: return
        p = cur / total
        w = 28
        bar = "█" * int(w*p) + "░" * (w - int(w*p))
        sys.stdout.write(
            "\r  " + Fore.RED + "[" + Fore.LIGHTRED_EX + bar + Fore.RED + "] " +
            Fore.WHITE + str(int(p*100)) + "% " +
            Fore.LIGHTBLACK_EX + desc[:30] + Style.RESET_ALL
        )
        sys.stdout.flush()
        if cur >= total: print()

    @classmethod
    def section(cls, title, icon="📌"):
        print()
        print("  " + Fore.RED + "╔" + "═" * 58 + "╗")
        print("  " + Fore.RED + "║ " + icon + " " + Fore.WHITE + Style.BRIGHT + title.ljust(54) + Fore.RED + "║")
        print("  " + Fore.RED + "╠" + "═" * 58 + "╣" + Style.RESET_ALL)

    @classmethod
    def result(cls, key, val, color=Fore.WHITE):
        print("  " + Fore.RED + "║ " + Fore.LIGHTYELLOW_EX + key.ljust(22) +
              Fore.WHITE + ": " + color + str(val)[:52] + Style.RESET_ALL)

    @classmethod
    def section_end(cls):
        print("  " + Fore.RED + "╚" + "═" * 58 + "╝" + Style.RESET_ALL)

    @classmethod
    def threat(cls, level, msg):
        icons = {"MALICIOUS": "🔴", "SUSPICIOUS": "🟠", "CLEAN": "🟢", "UNKNOWN": "⚪", "WARNING": "🟡"}
        colors = {"MALICIOUS": Fore.RED+Style.BRIGHT, "SUSPICIOUS": Fore.LIGHTRED_EX,
                  "CLEAN": Fore.GREEN, "UNKNOWN": Fore.WHITE, "WARNING": Fore.YELLOW}
        print("  " + Fore.RED + "║ " + icons.get(level,"⚪") + " " +
              colors.get(level,Fore.WHITE) + "[" + level + "] " +
              Fore.WHITE + msg[:48] + Style.RESET_ALL)

    @classmethod
    def stat_box(cls, stats):
        print()
        print("  " + Fore.LIGHTGREEN_EX + "╔" + "═" * 58 + "╗")
        print("  " + Fore.LIGHTGREEN_EX + "║" + Fore.WHITE + Style.BRIGHT + "  📊 SCAN SUMMARY".ljust(58) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╠" + "═" * 58 + "╣")
        for k, v in stats.items():
            print("  " + Fore.LIGHTGREEN_EX + "║  " + Fore.WHITE + k.ljust(25) + ": " +
                  Fore.LIGHTYELLOW_EX + str(v).ljust(28) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╚" + "═" * 58 + "╝" + Style.RESET_ALL)

    @classmethod
    def binary_reveal(cls, text):
        result = list(" " * len(text))
        indices = list(range(len(text)))
        random.shuffle(indices)
        for batch in range(0, len(indices), max(1, len(text)//6)):
            for idx in indices[batch:batch+max(1,len(text)//6)]:
                result[idx] = text[idx]
            d = ""
            for ch in result:
                d += (Fore.GREEN + random.choice("01")) if ch == " " else (Fore.LIGHTRED_EX + Style.BRIGHT + ch)
            sys.stdout.write("\r  " + d + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.06)
        print()
