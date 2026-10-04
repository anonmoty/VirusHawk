import re
from core.session import http
from core.vt_api import vt
from core.animator import Anim
from core.logger import Log
from engines.signature_db import SignatureDB
log = Log()

class URLScanner:
    @staticmethod
    def scan(url):
        Anim.section("URL THREAT SCAN: " + url[:40], "🔗")
        results = {"url": url, "threats": [], "vt_stats": None}

        # 1. Local pattern check
        Anim.scan_line("Pattern Analysis", "\033[33mscanning...\033[0m", "🧬")
        patterns = SignatureDB.scan_url_pattern(url)
        for p in patterns:
            results["threats"].append(p)
            Anim.threat(p["severity"], p["description"])

        # 2. URL structure analysis
        Anim.scan_line("URL Structure", "\033[33manalyzing...\033[0m", "🔬")
        if len(url) > 200:
            results["threats"].append({"description": "Abnormally long URL", "severity": "MEDIUM"})
            Anim.threat("MEDIUM", "Abnormally long URL (" + str(len(url)) + " chars)")
        if url.count("/") > 8:
            results["threats"].append({"description": "Deep path nesting", "severity": "LOW"})
        if "@" in url:
            results["threats"].append({"description": "@ symbol in URL (redirect trick)", "severity": "HIGH"})
            Anim.threat("HIGH", "@ symbol detected - possible redirect trick")

        # 3. HTTP response check
        Anim.scan_line("HTTP Response", "\033[33mchecking...\033[0m", "📡")
        r = http.get(url, allow_redirects=True)
        if r:
            Anim.result("Status", str(r.status_code))
            Anim.result("Final URL", r.url[:55])
            Anim.result("Server", r.headers.get("Server", "Hidden")[:30])

            # Check response body for threats
            body = r.text[:50000]
            code_findings = SignatureDB.scan_code(body)
            for f in code_findings:
                results["threats"].append(f)
                Anim.threat(f["severity"], f["description"])

            # Check for redirects to suspicious domains
            if r.url != url:
                Anim.result("Redirect", "Yes → " + r.url[:45], Fore.YELLOW)

            # Check for malware download
            ct = r.headers.get("Content-Type", "")
            if any(t in ct for t in ["application/octet-stream", "application/x-executable", "application/x-msdownload"]):
                results["threats"].append({"description": "Executable file download!", "severity": "CRITICAL"})
                Anim.threat("CRITICAL", "Executable file download detected!")
        else:
            Anim.result("Status", "No response / Blocked")

        # 4. VirusTotal check
        if vt.available():
            Anim.scan_line("VirusTotal", "\033[33mquerying...\033[0m", "🛡️")
            vt_data = vt.get_url_report(url)
            if vt_data:
                stats = vt.parse_stats(vt_data)
                results["vt_stats"] = stats
                if stats:
                    Anim.result("VT Malicious", str(stats["malicious"]), Fore.RED if stats["malicious"] > 0 else Fore.GREEN)
                    Anim.result("VT Suspicious", str(stats["suspicious"]), Fore.YELLOW if stats["suspicious"] > 0 else Fore.GREEN)
                    Anim.result("VT Clean", str(stats["harmless"]), Fore.GREEN)

                    detections = vt.parse_results(vt_data)
                    for d in detections[:5]:
                        Anim.threat("MALICIOUS" if d["category"] == "malicious" else "SUSPICIOUS",
                                    d["engine"] + ": " + d["result"])
        else:
            Anim.scan_line("VirusTotal", "\033[31mno API key\033[0m", "⚠️")

        # Verdict
        mal_count = len([t for t in results["threats"] if t.get("severity") in ["CRITICAL", "HIGH"]])
        if mal_count > 0:
            Anim.threat("MALICIOUS", str(mal_count) + " high/critical threats found!")
        elif results["threats"]:
            Anim.threat("SUSPICIOUS", str(len(results["threats"])) + " warnings found")
        else:
            Anim.threat("CLEAN", "No threats detected")

        Anim.section_end()
        return results

from colorama import Fore
