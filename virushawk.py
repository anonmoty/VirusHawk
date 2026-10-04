#!/usr/bin/env python3
"""
VirusHawk v1.0 - Threat Intelligence Scanner
VirusTotal + Local Engine | URL/File/Code/Endpoint/IP/Domain/Hash
Auto-Block Suspicious URLs | Termux Compatible
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Back, Style, init
init(autoreset=True)

from core.config import Config
from core.banner import Banner
from core.proxy import proxy
from core.vt_api import vt
from core.animator import Anim
from core.logger import Log

from engines.url_scanner import URLScanner
from engines.file_scanner import FileScanner
from engines.code_scanner import CodeScanner
from engines.endpoint_scanner import EndpointScanner
from engines.hash_scanner import HashScanner
from engines.ip_scanner import IPScanner
from engines.domain_scanner import DomainScanner
from engines.phishing_detect import PhishingDetector
from engines.url_blocker import URLBlocker
from output.reporter import Reporter

log = Log()


def setup_proxy():
    """Setup ProxyScrape proxy"""
    print()
    print("  " + Fore.MAGENTA + "🔌 Proxy Configuration")
    print("  " + Fore.WHITE + "  [1] Enable ProxyScrape (Recommended)")
    print("  " + Fore.WHITE + "  [2] Direct connection (No proxy)")
    print("  " + Fore.WHITE + "  [3] Custom proxy (ip:port)")
    ch = input("  " + Fore.GREEN + "└──╼ " + Style.RESET_ALL).strip()

    if ch == "1":
        proxy.on = True
        proxy.fetch()
    elif ch == "3":
        custom = input("  " + Fore.GREEN + "Proxy (ip:port): " + Style.RESET_ALL).strip()
        if custom:
            proxy.on = True
            proxy.alive = [custom]
            proxy.current = custom
            log.ok("Custom proxy: " + custom)
        else:
            proxy.on = False
    else:
        proxy.on = False
        log.info("Direct connection mode")


def setup_vt_key():
    """Setup VirusTotal API key"""
    Config.init()

    if Config.VT_API_KEY and len(Config.VT_API_KEY) > 20:
        vt.key = Config.VT_API_KEY
        log.ok("VirusTotal API key loaded (" + Config.VT_API_KEY[:8] + "...)")
        change = input("  " + Fore.YELLOW + "Change key? (y/n): " + Style.RESET_ALL).strip().lower()
        if change != "y":
            return

    print()
    print("  " + Fore.YELLOW + "╔" + "═" * 55 + "╗")
    print("  " + Fore.YELLOW + "║" + Fore.WHITE + "  🔑 VirusTotal API Key Setup" + " " * 25 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "╠" + "═" * 55 + "╣")
    print("  " + Fore.YELLOW + "║" + Fore.WHITE + "  Get FREE key:" + " " * 40 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "║" + Fore.CYAN + "  https://www.virustotal.com/gui/my-apikey" + " " * 13 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "║" + Fore.WHITE + "  1. Sign up / Login" + " " * 35 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "║" + Fore.WHITE + "  2. Click your profile → API Key" + " " * 22 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "║" + Fore.WHITE + "  3. Copy the 64-char key" + " " * 29 + Fore.YELLOW + "║")
    print("  " + Fore.YELLOW + "╚" + "═" * 55 + "╝" + Style.RESET_ALL)
    print()
    print("  " + Fore.WHITE + "  [1] Enter API key")
    print("  " + Fore.WHITE + "  [2] Skip (local scan only - no VirusTotal)")
    ch = input("  " + Fore.GREEN + "└──╼ " + Style.RESET_ALL).strip()

    if ch == "1":
        key = input("  " + Fore.GREEN + "Paste API key: " + Style.RESET_ALL).strip()
        if key and len(key) >= 32:
            Config.save_key(key)
            vt.key = key
            vt.available = lambda: True
            log.ok("API key saved & activated!")

            # Test key
            log.info("Testing API key...")
            test = vt.get_ip_report("8.8.8.8")
            if test:
                log.ok("API key is valid! ✅")
            else:
                log.warn("API key may be invalid or rate limited")
        else:
            log.warn("Key too short. Need 64-char key from VirusTotal")
    else:
        log.info("Running in LOCAL-ONLY mode (no VirusTotal)")
        log.info("Local signature engine still active ✅")


def show_menu():
    """Display main menu"""
    R = Fore.RED
    W = Fore.WHITE
    LR = Fore.LIGHTRED_EX
    LY = Fore.LIGHTYELLOW_EX
    LG = Fore.LIGHTGREEN_EX
    LC = Fore.LIGHTCYAN_EX
    LM = Fore.LIGHTMAGENTA_EX
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


def handle_url_scan():
    """Handle URL scanning with auto-block option"""
    url = input("\n  " + Fore.GREEN + "Enter URL to scan: " + Style.RESET_ALL).strip()
    if not url:
        log.warn("No URL provided")
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Check if already blocked
    if URLBlocker.check_blocklist(url):
        Anim.threat("WARNING", "This URL is already in your blocklist!")
        ans = input("  " + Fore.YELLOW + "Scan anyway? (y/n): " + Style.RESET_ALL).strip().lower()
        if ans != "y":
            return

    results = URLScanner.scan(url)

    if results:
        # Auto-block check
        threats = results.get("threats", [])
        vt_stats = results.get("vt_stats")
        crit = len([t for t in threats if t.get("severity") in ["CRITICAL", "MALICIOUS"]])
        high = len([t for t in threats if t.get("severity") == "HIGH"])
        vt_mal = 0
        if vt_stats and isinstance(vt_stats, dict):
            vt_mal = vt_stats.get("malicious", 0)

        total = crit + high + vt_mal

        if total >= 2:
            print()
            Anim.threat("MALICIOUS", str(total) + " threats! Auto-block recommended")
            ans = input("  " + Fore.RED + "Block this URL now? (y/n): " + Style.RESET_ALL).strip().lower()
            if ans == "y":
                reason = str(crit) + " critical, " + str(high) + " high, VT:" + str(vt_mal)
                URLBlocker.block_url(url, reason)
        elif total == 1:
            print()
            Anim.threat("SUSPICIOUS", "1 threat detected")
            ans = input("  " + Fore.YELLOW + "Block this URL? (y/n): " + Style.RESET_ALL).strip().lower()
            if ans == "y":
                URLBlocker.block_url(url, "Suspicious activity detected")

        # Save report
        path = Reporter.save("url_" + url[:20], results)
        log.ok("Report: " + path)


def handle_file_scan():
    """Handle file scanning"""
    path = input("\n  " + Fore.GREEN + "Enter file path: " + Style.RESET_ALL).strip()
    if not path:
        log.warn("No path")
        return

    # Expand ~ and relative paths
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    if not os.path.exists(path):
        log.err("File not found: " + path)
        return

    results = FileScanner.scan(path)
    if results:
        rp = Reporter.save("file_" + os.path.basename(path)[:20], results)
        log.ok("Report: " + rp)


def handle_code_scan():
    """Handle code scanning"""
    print("\n  " + Fore.CYAN + "[1] Scan a file")
    print("  " + Fore.CYAN + "[2] Paste code directly")
    m = input("  " + Fore.GREEN + "└──╼ " + Style.RESET_ALL).strip()

    if m == "1":
        path = input("  " + Fore.GREEN + "File path: " + Style.RESET_ALL).strip()
        if path:
            path = os.path.expanduser(path)
            CodeScanner.scan(filepath=path)
    elif m == "2":
        print("  " + Fore.CYAN + "Paste code (press Enter twice to finish):" + Style.RESET_ALL)
        lines = []
        empty_count = 0
        while True:
            line = input()
            if not line:
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        if lines:
            CodeScanner.scan(code="\n".join(lines))
    else:
        log.warn("Invalid choice")


def handle_endpoint_scan():
    """Handle endpoint scanning"""
    url = input("\n  " + Fore.GREEN + "Enter base URL: " + Style.RESET_ALL).strip()
    if not url:
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    EndpointScanner.scan(url)


def handle_hash_scan():
    """Handle hash lookup"""
    h = input("\n  " + Fore.GREEN + "Enter hash (MD5/SHA1/SHA256): " + Style.RESET_ALL).strip()
    if not h:
        return
    if len(h) not in [32, 40, 64]:
        log.warn("Hash length should be 32 (MD5), 40 (SHA1), or 64 (SHA256)")
    HashScanner.scan(h)


def handle_ip_scan():
    """Handle IP scanning"""
    ip = input("\n  " + Fore.GREEN + "Enter IP address: " + Style.RESET_ALL).strip()
    if not ip:
        return
    IPScanner.scan(ip)


def handle_domain_scan():
    """Handle domain scanning"""
    d = input("\n  " + Fore.GREEN + "Enter domain: " + Style.RESET_ALL).strip()
    if not d:
        return
    d = d.replace("https://", "").replace("http://", "").split("/")[0]
    DomainScanner.scan(d)


def handle_phishing_scan():
    """Handle phishing detection"""
    url = input("\n  " + Fore.GREEN + "Enter URL: " + Style.RESET_ALL).strip()
    if not url:
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    results = PhishingDetector.scan(url)

    if results and results.get("score", 0) >= 50:
        print()
        ans = input("  " + Fore.RED + "High phishing score! Block this URL? (y/n): " +
                    Style.RESET_ALL).strip().lower()
        if ans == "y":
            URLBlocker.block_url(url, "Phishing score: " + str(results["score"]))


def handle_block_url():
    """Handle manual URL blocking"""
    url = input("\n  " + Fore.GREEN + "Enter URL to BLOCK: " + Style.RESET_ALL).strip()
    if not url:
        return
    reason = input("  " + Fore.GREEN + "Reason (blank=Suspicious): " + Style.RESET_ALL).strip()
    if not reason:
        reason = "Manually blocked by user"
    URLBlocker.block_url(url, reason)


def handle_view_blocklist():
    """View blocked URLs"""
    URLBlocker.show_blocklist()


def handle_unblock():
    """Unblock a domain"""
    domain = input("\n  " + Fore.GREEN + "Enter domain to UNBLOCK: " + Style.RESET_ALL).strip()
    if not domain:
        return
    URLBlocker.unblock_url(domain)


def handle_scan_and_block():
    """Full scan + auto-block pipeline"""
    Anim.section("SCAN + AUTO-BLOCK MODE", "⚡")
    url = input("\n  " + Fore.GREEN + "Enter URL: " + Style.RESET_ALL).strip()
    if not url:
        Anim.section_end()
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    Anim.typing("  [*] Running full threat scan...", color=Fore.CYAN)

    # Step 1: URL Scan
    results = URLScanner.scan(url)

    if not results:
        Anim.threat("ERROR", "Scan failed")
        Anim.section_end()
        return

    # Step 2: Analyze threats
    threats = results.get("threats", [])
    vt_stats = results.get("vt_stats")

    crit = len([t for t in threats if t.get("severity") in ["CRITICAL", "MALICIOUS"]])
    high = len([t for t in threats if t.get("severity") == "HIGH"])
    med = len([t for t in threats if t.get("severity") == "MEDIUM"])
    vt_mal = 0
    if vt_stats and isinstance(vt_stats, dict):
        vt_mal = vt_stats.get("malicious", 0)

    total = crit + high + vt_mal

    print()
    Anim.stat_box({
        "🎯 URL": url[:45],
        "🔴 Critical": str(crit),
        "🟠 High": str(high),
        "🟡 Medium": str(med),
        "🛡️ VT Malicious": str(vt_mal),
        "📊 Total Threats": str(len(threats)),
    })

    # Step 3: Auto-block decision
    if total >= 3:
        Anim.threat("MALICIOUS", "DANGEROUS! Auto-blocking immediately!")
        reason = str(crit) + " critical, " + str(high) + " high, VT:" + str(vt_mal)
        URLBlocker.block_url(url, reason)

    elif total >= 1:
        Anim.threat("SUSPICIOUS", str(total) + " threats detected")
        ans = input("  " + Fore.RED + "Block this URL? (y/n): " + Style.RESET_ALL).strip().lower()
        if ans == "y":
            reason = str(crit) + " critical, " + str(high) + " high, VT:" + str(vt_mal)
            URLBlocker.block_url(url, reason)
        else:
            log.info("Skipped by user")

    else:
        Anim.threat("CLEAN", "URL appears safe. No blocking needed ✅")

    # Step 4: Phishing check
    print()
    Anim.typing("  [*] Running phishing check...", color=Fore.CYAN)
    phish_results = PhishingDetector.scan(url)
    if phish_results and phish_results.get("score", 0) >= 50:
        Anim.threat("MALICIOUS", "Phishing detected! Score: " + str(phish_results["score"]))
        ans = input("  " + Fore.RED + "Block for phishing? (y/n): " + Style.RESET_ALL).strip().lower()
        if ans == "y":
            URLBlocker.block_url(url, "Phishing score: " + str(phish_results["score"]))

    # Save combined report
    combined = {"url_scan": results, "phishing": phish_results}
    path = Reporter.save("full_scan_" + url[:20], combined)
    log.ok("Full report: " + path)

    Anim.section_end()


def generate_report():
    """Generate summary report"""
    log.info("Generating reports...")
    URLBlocker.init_files()

    # Count blocked URLs
    try:
        with open(URLBlocker.BLOCKLIST_FILE, "r") as f:
            blocked = len([l for l in f if l.strip() and not l.startswith("#")])
    except Exception:
        blocked = 0

    Anim.stat_box({
        "🦅 VirusHawk": "v1.0",
        "🚫 Blocked URLs": str(blocked),
        "🛡️ VT API": "Active" if vt.available() else "Inactive",
        "🔌 Proxy": "Active" if proxy.on else "Inactive",
        "📁 Reports": Config.REPORTS,
        "📋 Blocklist": URLBlocker.BLOCKLIST_FILE,
    })


def main():
    """Main entry point"""
    Config.init()
    Banner.show()

    # Initial setup
    setup_proxy()
    setup_vt_key()

    # Main loop
    while True:
        try:
            show_menu()

            print("  " + Fore.RED + "┌──(" + Fore.LIGHTRED_EX + "virushawk" + Fore.RED +
                  ")─[" + Fore.WHITE + "🦅" + Fore.RED + "]")
            choice = input("  " + Fore.RED + "└──╼ " + Fore.LIGHTRED_EX +
                           "Select: " + Style.RESET_ALL).strip()

            if choice == "99":
                print()
                Anim._typing("  [*] Saving blocklist...", speed=0.03, color=Fore.YELLOW)
                Anim._typing("  [*] Clearing traces...", speed=0.03, color=Fore.YELLOW)
                Anim._typing("  [*] VirusHawk shutting down.", speed=0.03, color=Fore.RED)
                print()
                print("  " + Fore.GREEN + "  🦅 Stay safe. Happy hunting!" + Style.RESET_ALL)
                print()
                sys.exit(0)

            elif choice == "77":
                setup_proxy()
                if proxy.on:
                    proxy.status()

            elif choice == "88":
                setup_vt_key()

            elif choice == "55":
                generate_report()

            elif choice in ["1", "01"]:
                handle_url_scan()

            elif choice in ["2", "02"]:
                handle_file_scan()

            elif choice in ["3", "03"]:
                handle_code_scan()

            elif choice in ["4", "04"]:
                handle_endpoint_scan()

            elif choice in ["5", "05"]:
                handle_hash_scan()

            elif choice in ["6", "06"]:
                handle_ip_scan()

            elif choice in ["7", "07"]:
                handle_domain_scan()

            elif choice in ["8", "08"]:
                handle_phishing_scan()

            elif choice in ["9", "09"]:
                handle_block_url()

            elif choice in ["10"]:
                handle_view_blocklist()

            elif choice in ["11"]:
                handle_unblock()

            elif choice in ["12"]:
                handle_scan_and_block()

            else:
                log.warn("Invalid option. Choose 01-12, 55, 77, 88, or 99")

        except KeyboardInterrupt:
            print()
            print()
            Anim._typing("  [*] Interrupted! Saving data...", speed=0.03, color=Fore.RED)
            try:
                generate_report()
            except Exception:
                pass
            print("  " + Fore.GREEN + "  🦅 Goodbye!" + Style.RESET_ALL)
            sys.exit(0)

        except Exception as e:
            log.err("Fatal error: " + str(e))
            import traceback
            traceback.print_exc()
            time.sleep(1)
            continue


if __name__ == "__main__":
    main()
