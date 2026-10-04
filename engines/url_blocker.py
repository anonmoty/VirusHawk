#!/usr/bin/env python3
"""VirusHawk - URL Blocker & Takedown Engine"""

import os
import re
import time
from urllib.parse import urlparse
from datetime import datetime
from core.config import Config
from core.session import http
from core.animator import Anim
from core.logger import Log

log = Log()


class URLBlocker:
    """Block, blacklist, and report malicious URLs"""

    BLOCKLIST_FILE = os.path.join(Config.BASE, "blocklist.txt")
    TAKEDOWN_LOG = os.path.join(Config.BASE, "takedown_log.txt")

    @classmethod
    def init_files(cls):
        Config.init()
        if not os.path.exists(cls.BLOCKLIST_FILE):
            with open(cls.BLOCKLIST_FILE, "w") as f:
                f.write("# VirusHawk Blocklist\n")
                f.write("# Auto-generated - Do not edit manually\n")
                f.write("# Format: DOMAIN | REASON | DATE\n\n")
        if not os.path.exists(cls.TAKEDOWN_LOG):
            with open(cls.TAKEDOWN_LOG, "w") as f:
                f.write("# VirusHawk Takedown Log\n\n")

    @classmethod
    def block_url(cls, url, reason="Suspicious"):
        """Block a URL by adding to local blocklist + hosts file"""
        cls.init_files()

        parsed = urlparse(url if "://" in url else "http://" + url)
        domain = parsed.hostname
        if not domain:
            Anim.threat("ERROR", "Cannot extract domain from URL")
            return False

        Anim.section("URL BLOCKER: " + domain, "🚫")

        # Step 1: Add to VirusHawk blocklist
        Anim.scan_line("Blocklist", "\033[33madding...\033[0m", "📋")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = domain + " | " + reason + " | " + ts + "\n"

        with open(cls.BLOCKLIST_FILE, "a") as f:
            f.write(entry)
        Anim.threat("MALICIOUS", "Added to blocklist: " + domain)

        # Step 2: Try to add to /etc/hosts (needs root)
        Anim.scan_line("Hosts File", "\033[33mblocking...\033[0m", "🔒")
        hosts_entry = "127.0.0.1 " + domain + "\n"
        hosts_blocked = False
        try:
            with open("/etc/hosts", "r") as f:
                hosts_content = f.read()
            if domain not in hosts_content:
                with open("/etc/hosts", "a") as f:
                    f.write(hosts_entry)
                hosts_blocked = True
                Anim.threat("MALICIOUS", "Blocked in /etc/hosts → 127.0.0.1")
            else:
                Anim.result("Hosts", "Already blocked")
                hosts_blocked = True
        except PermissionError:
            Anim.result("Hosts", "No root access (run with sudo)", Fore.YELLOW)
            # Fallback: save hosts entry for manual use
            hosts_backup = os.path.join(Config.BASE, "hosts_block.txt")
            with open(hosts_backup, "a") as f:
                f.write(hosts_entry)
            Anim.result("Fallback", "Saved to " + hosts_backup, Fore.CYAN)
        except Exception as e:
            Anim.result("Hosts", "Error: " + str(e)[:40], Fore.YELLOW)

        # Step 3: Generate iptables rule (if available)
        Anim.scan_line("Firewall", "\033[33mgenerating rule...\033[0m", "🧱")
        import socket
        try:
            ip = socket.gethostbyname(domain)
            iptables_rule = "iptables -A OUTPUT -d " + ip + " -j DROP"
            Anim.result("IP", ip)
            Anim.result("Rule", iptables_rule, Fore.LIGHTRED_EX)

            # Try to apply
            ret = os.system(iptables_rule + " 2>/dev/null")
            if ret == 0:
                Anim.threat("MALICIOUS", "Firewall rule applied! IP blocked.")
            else:
                # Save rule for manual use
                fw_file = os.path.join(Config.BASE, "firewall_rules.txt")
                with open(fw_file, "a") as f:
                    f.write("# Block " + domain + " (" + ip + ")\n")
                    f.write(iptables_rule + "\n")
                    f.write("ip6tables -A OUTPUT -d " + ip + " -j DROP\n\n")
                Anim.result("Firewall", "Rule saved to firewall_rules.txt", Fore.CYAN)
        except Exception:
            Anim.result("Firewall", "Could not resolve IP", Fore.YELLOW)

        # Step 4: Log takedown action
        Anim.scan_line("Takedown Log", "\033[33mlogging...\033[0m", "📝")
        takedown_entry = (
            "\n" + "=" * 60 + "\n"
            "URL: " + url + "\n"
            "Domain: " + domain + "\n"
            "Reason: " + reason + "\n"
            "Blocked: " + ts + "\n"
            "Hosts: " + ("Yes" if hosts_blocked else "No (no root)") + "\n"
            "Status: BLOCKED\n"
        )
        with open(cls.TAKEDOWN_LOG, "a") as f:
            f.write(takedown_entry)

        # Step 5: Generate abuse report
        Anim.scan_line("Abuse Report", "\033[33mgenerating...\033[0m", "📧")
        abuse_info = cls._generate_abuse_info(domain, url, reason)
        if abuse_info:
            Anim.result("Abuse Email", abuse_info.get("email", "N/A"), Fore.CYAN)
            Anim.result("Registrar", abuse_info.get("registrar", "N/A"))

        # Final summary
        print()
        Anim.threat("MALICIOUS", "URL BLOCKED SUCCESSFULLY!")
        Anim.result("🚫 Domain", domain, Fore.RED)
        Anim.result("📋 Blocklist", cls.BLOCKLIST_FILE, Fore.CYAN)
        Anim.result("📝 Log", cls.TAKEDOWN_LOG, Fore.CYAN)

        Anim.section_end()
        return True

    @classmethod
    def _generate_abuse_info(cls, domain, url, reason):
        """Generate abuse contact info for reporting"""
        info = {}
        try:
            import whois
            w = whois.whois(domain)
            info["registrar"] = str(w.registrar or "N/A")
            emails = w.emails
            if emails:
                if isinstance(emails, list):
                    abuse_emails = [e for e in emails if "abuse" in e.lower()]
                    info["email"] = abuse_emails[0] if abuse_emails else emails[0]
                else:
                    info["email"] = str(emails)
        except Exception:
            # Fallback
            info["registrar"] = "Check whois.domaintools.com"
            info["email"] = "abuse@" + domain

        # Save abuse report
        report_path = os.path.join(Config.BASE, "abuse_report_" + domain.replace(".", "_") + ".txt")
        with open(report_path, "w") as f:
            f.write("ABUSE REPORT - Generated by VirusHawk\n")
            f.write("=" * 60 + "\n\n")
            f.write("To: " + info.get("email", "abuse@" + domain) + "\n")
            f.write("Subject: Abuse Report - Malicious Domain: " + domain + "\n\n")
            f.write("Dear Abuse Team,\n\n")
            f.write("We have identified the following domain as malicious:\n\n")
            f.write("Domain: " + domain + "\n")
            f.write("URL: " + url + "\n")
            f.write("Reason: " + reason + "\n")
            f.write("Detected: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write("This domain has been flagged for suspicious/malicious activity.\n")
            f.write("Please investigate and take appropriate action.\n\n")
            f.write("Regards,\nVirusHawk Threat Intelligence\n")
        Anim.result("Report", report_path, Fore.CYAN)

        return info

    @classmethod
    def check_blocklist(cls, url):
        """Check if URL is already in blocklist"""
        cls.init_files()
        parsed = urlparse(url if "://" in url else "http://" + url)
        domain = parsed.hostname
        if not domain:
            return False

        try:
            with open(cls.BLOCKLIST_FILE, "r") as f:
                content = f.read()
            if domain in content:
                return True
        except Exception:
            pass
        return False

    @classmethod
    def show_blocklist(cls):
        """Display current blocklist"""
        cls.init_files()
        Anim.section("CURRENT BLOCKLIST", "🚫")
        try:
            with open(cls.BLOCKLIST_FILE, "r") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            if lines:
                for i, line in enumerate(lines, 1):
                    Anim.result(str(i), line[:65], Fore.RED)
                Anim.result("Total", str(len(lines)) + " blocked domains")
            else:
                Anim.result("Status", "Blocklist is empty")
        except Exception as e:
            Anim.result("Error", str(e)[:50])
        Anim.section_end()

    @classmethod
    def unblock_url(cls, domain):
        """Remove domain from blocklist"""
        cls.init_files()
        try:
            with open(cls.BLOCKLIST_FILE, "r") as f:
                lines = f.readlines()
            new_lines = [l for l in lines if domain not in l or l.startswith("#")]
            with open(cls.BLOCKLIST_FILE, "w") as f:
                f.writelines(new_lines)
            Anim.threat("CLEAN", "Unblocked: " + domain)

            # Remove from hosts
            try:
                with open("/etc/hosts", "r") as f:
                    hosts = f.readlines()
                new_hosts = [l for l in hosts if domain not in l]
                with open("/etc/hosts", "w") as f:
                    f.writelines(new_hosts)
                Anim.threat("CLEAN", "Removed from /etc/hosts")
            except Exception:
                pass
        except Exception as e:
            Anim.result("Error", str(e)[:50])

    @classmethod
    def auto_block_from_scan(cls, scan_results, url):
        """Auto-block if scan found critical threats"""
        threats = scan_results.get("threats", [])
        vt_stats = scan_results.get("vt_stats", {})

        should_block = False
        reasons = []

        # Check local threats
        critical = [t for t in threats if t.get("severity") in ["CRITICAL", "MALICIOUS"]]
        if len(critical) >= 2:
            should_block = True
            reasons.append(str(len(critical)) + " critical threats")

        # Check VT stats
        if vt_stats and isinstance(vt_stats, dict):
            mal = vt_stats.get("malicious", 0)
            if mal >= 3:
                should_block = True
                reasons.append("VT: " + str(mal) + " engines flagged")

        if should_block:
            reason = " | ".join(reasons) if reasons else "Multiple threats"
            print()
            Anim.threat("MALICIOUS", "Auto-block triggered! Reason: " + reason)
            ans = input("  " + Fore.RED + "Block this URL? (y/n): " + Style.RESET_ALL).strip().lower()
            if ans == "y":
                cls.block_url(url, reason)
            else:
                Anim.result("Status", "Skipped by user", Fore.YELLOW)

from colorama import Fore, Style
