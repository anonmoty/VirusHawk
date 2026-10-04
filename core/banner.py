#!/usr/bin/env python3
"""VirusHawk - Professional Hacker Banner"""

import sys
import time
import os
import random
import shutil
from colorama import Fore, Back, Style, init

init(autoreset=True)


class Banner:

    @staticmethod
    def _w():
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    @classmethod
    def _matrix(cls, dur=1.0):
        w = min(cls._w(), 85)
        chars = "01アイウエオカキクケコサシスセソ"
        end = time.time() + dur
        while time.time() < end:
            line = ""
            for _ in range(w):
                r = random.random()
                if r < 0.08:
                    line += Fore.LIGHTGREEN_EX + random.choice(chars)
                elif r < 0.12:
                    line += Fore.GREEN + random.choice("01")
                else:
                    line += " "
            print(line + Style.RESET_ALL)
            time.sleep(0.02)

    @classmethod
    def _glitch(cls, text, n=2):
        g = "▓▒░█▄▀■□╳╬"
        for _ in range(n):
            out = ""
            for ch in text:
                if ch != " " and random.random() < 0.15:
                    out += random.choice([Fore.RED, Fore.CYAN, Fore.GREEN]) + random.choice(g)
                else:
                    out += Fore.LIGHTRED_EX + ch
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write("\r" + Fore.LIGHTRED_EX + text + Style.RESET_ALL + "\n")

    @classmethod
    def _typing(cls, text, speed=0.02, color=Fore.GREEN):
        for ch in text:
            sys.stdout.write(color + ch)
            sys.stdout.flush()
            time.sleep(speed + random.uniform(0, 0.015))
        print(Style.RESET_ALL)

    @classmethod
    def _binary_reveal(cls, text):
        result = list(" " * len(text))
        indices = list(range(len(text)))
        random.shuffle(indices)
        steps = max(1, len(text) // 6)
        for batch in range(0, len(indices), steps):
            for idx in indices[batch:batch + steps]:
                result[idx] = text[idx]
            d = ""
            for ch in result:
                if ch == " ":
                    d += Fore.GREEN + random.choice("01")
                else:
                    d += Fore.LIGHTRED_EX + Style.BRIGHT + ch
            sys.stdout.write("\r  " + d + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.06)
        print()

    @classmethod
    def show(cls):
        os.system("clear" if os.name == "posix" else "cls")
        cls._matrix(0.8)
        os.system("clear" if os.name == "posix" else "cls")

        # Loading animation
        for i in range(20):
            sp = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[i % 10]
            sys.stdout.write(
                "\r  " + Fore.RED + sp + Fore.WHITE +
                " Loading threat engines [" + str(i * 5) + "%]"
            )
            sys.stdout.flush()
            time.sleep(0.06)
        print("\r  " + Fore.GREEN + "✓ All threat engines armed!              ")
        time.sleep(0.3)

        # Main logo
        logo = [
            "",
            Fore.LIGHTRED_EX + Style.BRIGHT +
            "   ██╗   ██╗██╗██████╗ ██╗   ██╗███████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗",
            Fore.LIGHTRED_EX + Style.BRIGHT +
            "   ██║   ██║██║██╔══██╗██║   ██║██╔════╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝",
            Fore.RED + Style.BRIGHT +
            "   ██║   ██║██║██████╔╝██║   ██║███████╗███████║███████║██║ █╗ ██║█████╔╝ ",
            Fore.RED + Style.BRIGHT +
            "   ╚██╗ ██╔╝██║██╔══██╗██║   ██║╚════██║██╔══██║██╔══██║██║███╗██║██╔═██╗ ",
            Fore.RED +
            "    ╚████╔╝ ██║██║  ██║╚██████╔╝███████║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗",
            Fore.RED +
            "     ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝",
            "",
        ]
        for line in logo:
            cls._glitch(line, n=2)
            time.sleep(0.01)

        # Hawk ASCII
        hawk = [
            Fore.LIGHTRED_EX + "              ,___,",
            Fore.LIGHTRED_EX + "              [O.o]  ← threat detected",
            Fore.LIGHTRED_EX + "              /)  )",
            Fore.LIGHTRED_EX + "              d\"\"b",
            Fore.RED + Style.BRIGHT + "           Devloper MAXOD",
        ]
        for line in hawk:
            print("  " + line + Style.RESET_ALL)
            time.sleep(0.04)

        print()

        # Info box
        info = [
            Fore.RED + "    ╔" + "═" * 66 + "╗",
            Fore.RED + "    ║" + Fore.LIGHTRED_EX + " 🦅 VirusHawk v1.0 " + Fore.LIGHTBLACK_EX + "│" +
            Fore.LIGHTYELLOW_EX + " Threat Intelligence Scanner          " + Fore.RED + "   ║",
            Fore.RED + "    ╠" + "═" * 66 + "╣",
            Fore.RED + "    ║" + Fore.WHITE +
            " 🔍 Scanners : URL|File|Code|Endpoint|IP|Domain|Hash " + Fore.RED + "       ║",
            Fore.RED + "    ║" + Fore.WHITE +
            " 🛡️ Engines  : VirusTotal API + Local Signatures     " + Fore.RED + "       ║",
            Fore.RED + "    ║" + Fore.WHITE +
            " 🚫 Blocker  : Auto-Block + Hosts + Firewall         " + Fore.RED + "       ║",
            Fore.RED + "    ║" + Fore.WHITE +
            " 🔌 Proxy    : ProxyScrape Rotation                  " + Fore.RED + "       ║",
            Fore.RED + "    ║" + Fore.WHITE +
            " 💀 Status   : ARMED & HUNTING 🔴                    " + Fore.RED + "       ║",
            Fore.RED + "    ╚" + "═" * 66 + "╝",
        ]
        for line in info:
            print(line)
            time.sleep(0.03)
        print(Style.RESET_ALL)

        cls._binary_reveal("[ VIRUSHAWK - THREAT DETECTION ACTIVE ]")
        print()

    @classmethod
    def menu(cls):
        R = Fore.RED
        W = Fore.WHITE
        LR = Fore.LIGHTRED_EX
        LY = Fore.LIGHTYELLOW_EX
        LG = Fore.LIGHTGREEN_EX
        LC = Fore.LIGHTCYAN_EX
        LM = Fore.LIGHTMAGENTA_EX
        LB = Fore.LIGHTBLACK_EX
        S = Style.RESET_ALL

        lines = [
            "",
            R + "  ╔" + "═" * 68 + "╗",
            R + "  ║" + LR + Style.BRIGHT +
            "               🦅 VIRUSHAWK COMMAND CENTER 🦅                    " + R + " ║",
            R + "  ╠" + "═" * 68 + "╣",
            R + "  ║ " + LY + "━━ THREAT SCANNERS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ " + R + "  ║",
            R + "  ║  " + LR + "[01]" + W + " 🔗 URL Scanner         " + LR + "[02]" + W +
            " 📁 File Scanner         " + R + "   ║",
            R + "  ║  " + LR + "[03]" + W + " 💻 Code Scanner        " + LR + "[04]" + W +
            " 🎯 Endpoint Scanner     " + R + "   ║",
            R + "  ║  " + LR + "[05]" + W + " 🔐 Hash Lookup         " + LR + "[06]" + W +
            " 🌐 IP Scanner          " + R + "   ║",
            R + "  ║  " + LR + "[07]" + W + " 🌍 Domain Scanner      " + LR + "[08]" + W +
            " 🎣 Phishing Detect     " + R + "   ║",
            R + "  ║ " + LY + "━━ URL BLOCKER & TAKEDOWN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ " + R + "  ║",
            R + "  ║  " + LR + "[09]" + W + " 🚫 Block URL           " + LR + "[10]" + W +
            " 📋 View Blocklist       " + R + "   ║",
            R + "  ║  " + LR + "[11]" + W + " ✅ Unblock Domain      " + LR + "[12]" + W +
            " ⚡ Scan + Auto-Block    " + R + "   ║",
            R + "  ╠" + "═" * 68 + "╣",
            R + "  ║  " + LY + "[77]" + LC + " 🔌 Proxy Settings      " + LY + "[88]" + LM +
            " 🔑 VT API Key Setup    " + R + "   ║",
            R + "  ║  " + LY + "[55]" + LY + " 📊 Generate Report     " + LY + "[99]" + LR +
            " 🚪 Exit                " + R + "   ║",
            R + "  ╚" + "═" * 68 + "╝",
            S,
        ]
        for line in lines:
            print(line)

    @classmethod
    def section(cls, title, icon="📌"):
        w = 58
        print()
        print("  " + Fore.RED + "╔" + "═" * w + "╗")
        print("  " + Fore.RED + "║ " + icon + " " +
              Fore.WHITE + Style.BRIGHT + title.ljust(w - 4) + Fore.RED + "║")
        print("  " + Fore.RED + "╠" + "═" * w + "╣" + Style.RESET_ALL)

    @classmethod
    def result(cls, key, val, color=Fore.WHITE):
        print("  " + Fore.RED + "║ " + Fore.LIGHTYELLOW_EX + key.ljust(22) +
              Fore.WHITE + ": " + color + str(val)[:52] + Style.RESET_ALL)

    @classmethod
    def section_end(cls):
        print("  " + Fore.RED + "╚" + "═" * 58 + "╝" + Style.RESET_ALL)

    @classmethod
    def threat(cls, level, msg):
        icons = {
            "MALICIOUS": "🔴", "SUSPICIOUS": "🟠", "CLEAN": "🟢",
            "UNKNOWN": "⚪", "WARNING": "🟡", "ERROR": "❌", "INFO": "🔵",
        }
        colors = {
            "MALICIOUS": Fore.RED + Style.BRIGHT,
            "SUSPICIOUS": Fore.LIGHTRED_EX,
            "CLEAN": Fore.GREEN,
            "UNKNOWN": Fore.WHITE,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "INFO": Fore.CYAN,
        }
        icon = icons.get(level, "⚪")
        color = colors.get(level, Fore.WHITE)
        print("  " + Fore.RED + "║ " + icon + " " +
              color + "[" + level + "] " +
              Fore.WHITE + msg[:48] + Style.RESET_ALL)

    @classmethod
    def stat_box(cls, stats):
        w = 58
        print()
        print("  " + Fore.LIGHTGREEN_EX + "╔" + "═" * w + "╗")
        print("  " + Fore.LIGHTGREEN_EX + "║" + Fore.WHITE + Style.BRIGHT +
              "  📊 SCAN SUMMARY".ljust(w) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╠" + "═" * w + "╣")
        for k, v in stats.items():
            print("  " + Fore.LIGHTGREEN_EX + "║  " + Fore.WHITE +
                  k.ljust(25) + ": " + Fore.LIGHTYELLOW_EX +
                  str(v).ljust(w - 30) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╚" + "═" * w + "╝" + Style.RESET_ALL)

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
        if total == 0:
            return
        p = cur / total
        w = 28
        bar = "█" * int(w * p) + "░" * (w - int(w * p))
        sys.stdout.write(
            "\r  " + Fore.RED + "[" + Fore.LIGHTRED_EX + bar + Fore.RED + "] " +
            Fore.WHITE + str(int(p * 100)) + "% " +
            Fore.LIGHTBLACK_EX + desc[:30] + Style.RESET_ALL
        )
        sys.stdout.flush()
        if cur >= total:
            print()
