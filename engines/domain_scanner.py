from core.vt_api import vt
from core.session import http
from core.animator import Anim
from core.logger import Log
log = Log()

class DomainScanner:
    @staticmethod
    def scan(domain):
        Anim.section("DOMAIN THREAT SCAN", "🌐")
        domain = domain.replace("https://", "").replace("http://", "").split("/")[0].replace("www.", "")
        results = {"domain": domain, "threats": []}

        Anim.result("Domain", domain)

        # VirusTotal
        if vt.available():
            Anim.scan_line("VirusTotal", "\033[33mquerying...\033[0m", "🛡️")
            vt_data = vt.get_domain_report(domain)
            if vt_data:
                stats = vt.parse_stats(vt_data)
                if stats:
                    Anim.result("VT Malicious", str(stats["malicious"]),
                                Fore.RED if stats["malicious"] > 0 else Fore.GREEN)
                    Anim.result("VT Suspicious", str(stats["suspicious"]))
                    Anim.result("VT Clean", str(stats["harmless"]), Fore.GREEN)

                # Categories
                cats = vt_data.get("categories", {})
                if cats:
                    Anim.result("Categories", str(cats)[:60])

                # WHOIS
                registrar = vt_data.get("registrar", "")
                if registrar: Anim.result("Registrar", registrar)

                creation = vt_data.get("creation_date", 0)
                if creation:
                    from datetime import datetime
                    try:
                        dt = datetime.fromtimestamp(creation)
                        Anim.result("Created", dt.strftime("%Y-%m-%d"))
                        age = (datetime.now() - dt).days
                        Anim.result("Age", str(age) + " days")
                        if age < 30:
                            Anim.threat("WARNING", "Very new domain (< 30 days)")
                            results["threats"].append({"description": "New domain", "severity": "MEDIUM"})
                    except: pass

                detections = vt.parse_results(vt_data)
                for d in detections[:5]:
                    Anim.threat("MALICIOUS", d["engine"] + ": " + d["result"])
        else:
            Anim.scan_line("VirusTotal", "\033[31mno API key\033[0m", "⚠️")

        Anim.section_end()
        return results

from colorama import Fore
