from core.vt_api import vt
from core.animator import Anim
from core.logger import Log
log = Log()

class HashScanner:
    @staticmethod
    def scan(file_hash):
        Anim.section("HASH LOOKUP", "🔐")
        Anim.result("Hash", file_hash[:60])
        results = {"hash": file_hash, "vt_stats": None}

        if not vt.available():
            Anim.threat("ERROR", "VirusTotal API key required for hash lookup")
            Anim.section_end()
            return results

        Anim.scan_line("VirusTotal", "\033[33mquerying...\033[0m", "🛡️")
        vt_data = vt.get_file_report(file_hash)

        if vt_data:
            stats = vt.parse_stats(vt_data)
            results["vt_stats"] = stats

            Anim.result("Type", vt_data.get("type_tag", "unknown"))
            Anim.result("Size", str(vt_data.get("size", 0)) + " bytes")
            Anim.result("Names", str(vt_data.get("meaningful_names", []))[:50])

            if stats:
                Anim.result("Malicious", str(stats["malicious"]),
                            Fore.RED if stats["malicious"] > 0 else Fore.GREEN)
                Anim.result("Suspicious", str(stats["suspicious"]),
                            Fore.YELLOW if stats["suspicious"] > 0 else Fore.GREEN)
                Anim.result("Clean", str(stats["harmless"]), Fore.GREEN)
                Anim.result("Undetected", str(stats["undetected"]))

            detections = vt.parse_results(vt_data)
            if detections:
                Anim.result("Detections", str(len(detections)) + " engines flagged")
                for d in detections[:8]:
                    Anim.threat("MALICIOUS" if d["category"] == "malicious" else "SUSPICIOUS",
                                d["engine"] + ": " + d["result"])

            if stats and stats["malicious"] > 0:
                Anim.threat("MALICIOUS", "Detected by " + str(stats["malicious"]) + " engines!")
            else:
                Anim.threat("CLEAN", "No detections")
        else:
            Anim.threat("UNKNOWN", "Hash not found in VirusTotal database")

        Anim.section_end()
        return results

from colorama import Fore
