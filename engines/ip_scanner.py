import socket
from core.vt_api import vt
from core.session import http
from core.animator import Anim
from core.logger import Log
log = Log()

class IPScanner:
    @staticmethod
    def scan(ip):
        Anim.section("IP THREAT SCAN", "🌐")
        results = {"ip": ip, "threats": []}

        # GeoIP
        Anim.scan_line("GeoIP", "\033[33mlocating...\033[0m", "🌍")
        try:
            r = http.get("http://ip-api.com/json/" + ip)
            if r and r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    Anim.result("Country", d.get("country", "") + " (" + d.get("countryCode", "") + ")")
                    Anim.result("City", d.get("city", ""))
                    Anim.result("ISP", d.get("isp", ""))
                    Anim.result("Org", d.get("org", ""))
                    Anim.result("AS", d.get("as", ""))
                    if d.get("proxy"):
                        Anim.threat("WARNING", "IP is a proxy/VPN")
                        results["threats"].append({"description": "Proxy/VPN IP", "severity": "MEDIUM"})
                    if d.get("hosting"):
                        Anim.threat("INFO", "Hosting/datacenter IP")
        except: pass

        # Reverse DNS
        Anim.scan_line("Reverse DNS", "\033[33mresolving...\033[0m", "🔄")
        try:
            hostname = socket.gethostbyaddr(ip)
            Anim.result("Hostname", hostname[0])
        except:
            Anim.result("Hostname", "No reverse DNS")

        # VirusTotal
        if vt.available():
            Anim.scan_line("VirusTotal", "\033[33mquerying...\033[0m", "🛡️")
            vt_data = vt.get_ip_report(ip)
            if vt_data:
                stats = vt.parse_stats(vt_data)
                if stats:
                    Anim.result("VT Malicious", str(stats["malicious"]),
                                Fore.RED if stats["malicious"] > 0 else Fore.GREEN)
                    Anim.result("VT Suspicious", str(stats["suspicious"]))
                    Anim.result("VT Clean", str(stats["harmless"]), Fore.GREEN)

                # ASN info
                asn = vt_data.get("asn", "")
                network = vt_data.get("network", "")
                if asn: Anim.result("ASN", str(asn))
                if network: Anim.result("Network", network)

                # WHOIS
                whois = vt_data.get("whois", "")
                if whois:
                    Anim.result("WHOIS", whois[:60])

                detections = vt.parse_results(vt_data)
                for d in detections[:5]:
                    Anim.threat("MALICIOUS", d["engine"] + ": " + d["result"])
                    results["threats"].append({"description": d["engine"] + ": " + d["result"], "severity": "HIGH"})
        else:
            Anim.scan_line("VirusTotal", "\033[31mno API key\033[0m", "⚠️")

        Anim.section_end()
        return results

from colorama import Fore
