import os, hashlib
from core.vt_api import vt
from core.animator import Anim
from core.logger import Log
from engines.signature_db import SignatureDB
log = Log()

class FileScanner:
    @staticmethod
    def scan(filepath):
        Anim.section("FILE THREAT SCAN", "📁")

        if not os.path.exists(filepath):
            Anim.threat("ERROR", "File not found: " + filepath)
            Anim.section_end()
            return None

        results = {"file": filepath, "threats": [], "hashes": {}, "vt_stats": None}

        # File info
        size = os.path.getsize(filepath)
        Anim.result("File", os.path.basename(filepath))
        Anim.result("Size", str(size) + " bytes (" + str(round(size/1024, 2)) + " KB)")
        Anim.result("Path", filepath[:55])

        # Calculate hashes
        Anim.scan_line("Hashing", "\033[33mcalculating...\033[0m", "🔐")
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            md5 = hashlib.md5(content).hexdigest()
            sha1 = hashlib.sha1(content).hexdigest()
            sha256 = hashlib.sha256(content).hexdigest()
            results["hashes"] = {"MD5": md5, "SHA1": sha1, "SHA256": sha256}
            Anim.result("MD5", md5)
            Anim.result("SHA1", sha1)
            Anim.result("SHA256", sha256[:50] + "...")
        except Exception as e:
            Anim.result("Hash Error", str(e)[:40])
            Anim.section_end()
            return results

        # Magic bytes detection
        Anim.scan_line("File Type", "\033[33manalyzing...\033[0m", "🔬")
        magic = content[:16]
        file_type = "Unknown"
        if magic[:4] == b'\x7fELF': file_type = "Linux ELF Executable ⚠️"
        elif magic[:2] == b'MZ': file_type = "Windows PE Executable ⚠️"
        elif magic[:4] == b'PK\x03\x04': file_type = "ZIP/Archive/JAR/APK/DOCX"
        elif magic[:3] == b'\xff\xd8\xff': file_type = "JPEG Image"
        elif magic[:8] == b'\x89PNG\r\n\x1a\n': file_type = "PNG Image"
        elif magic[:4] == b'GIF8': file_type = "GIF Image"
        elif magic[:5] == b'%PDF-': file_type = "PDF Document"
        elif magic[:4] == b'<?ph' or magic[:5] == b'<?php': file_type = "PHP Script ⚠️"
        elif b'<html' in content[:500].lower() or b'<!doctype' in content[:500].lower(): file_type = "HTML Document"
        elif b'<script' in content[:1000].lower(): file_type = "JavaScript/HTML ⚠️"
        elif magic[:2] == b'#!': file_type = "Shell Script ⚠️"
        Anim.result("Type", file_type)

        if "Executable" in file_type or "Script" in file_type:
            results["threats"].append({"description": "Executable/script file type", "severity": "WARNING"})

        # Local signature scan
        Anim.scan_line("Signature Scan", "\033[33mscanning...\033[0m", "🧬")
        try:
            text_content = content.decode("utf-8", errors="ignore")
            findings = SignatureDB.scan_code(text_content)
            for f in findings:
                results["threats"].append(f)
                Anim.threat(f["severity"], f["description"] + " (" + str(f["matches"]) + "x)")
        except: pass

        # Entropy analysis (high entropy = possible encryption/packing)
        Anim.scan_line("Entropy", "\033[33manalyzing...\033[0m", "📊")
        import math
        if len(content) > 0:
            freq = {}
            for byte in content[:10000]:
                freq[byte] = freq.get(byte, 0) + 1
            entropy = -sum((c/len(content[:10000])) * math.log2(c/len(content[:10000])) for c in freq.values())
            Anim.result("Entropy", str(round(entropy, 2)) + " / 8.0")
            if entropy > 7.0:
                results["threats"].append({"description": "Very high entropy (packed/encrypted)", "severity": "HIGH"})
                Anim.threat("HIGH", "High entropy - possibly packed/encrypted malware")
            elif entropy > 6.0:
                Anim.threat("WARNING", "Moderate entropy - may be compressed")

        # VirusTotal
        if vt.available():
            Anim.scan_line("VirusTotal", "\033[33mquerying hash...\033[0m", "🛡️")
            vt_data = vt.get_file_report(sha256)
            if vt_data:
                stats = vt.parse_stats(vt_data)
                results["vt_stats"] = stats
                if stats:
                    Anim.result("VT Malicious", str(stats["malicious"]), Fore.RED if stats["malicious"] > 0 else Fore.GREEN)
                    Anim.result("VT Suspicious", str(stats["suspicious"]))
                    Anim.result("VT Clean", str(stats["harmless"]), Fore.GREEN)
                    detections = vt.parse_results(vt_data)
                    for d in detections[:5]:
                        Anim.threat("MALICIOUS", d["engine"] + ": " + d["result"])
            else:
                Anim.result("VT", "Not found in database (new file?)")
        else:
            Anim.scan_line("VirusTotal", "\033[31mno API key\033[0m", "⚠️")

        # Verdict
        mal = len([t for t in results["threats"] if t.get("severity") in ["CRITICAL", "HIGH"]])
        if mal > 0: Anim.threat("MALICIOUS", str(mal) + " critical/high threats!")
        elif results["threats"]: Anim.threat("SUSPICIOUS", str(len(results["threats"])) + " warnings")
        else: Anim.threat("CLEAN", "No threats detected")

        Anim.section_end()
        return results

from colorama import Fore
