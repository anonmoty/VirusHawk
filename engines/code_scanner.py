from core.animator import Anim
from core.logger import Log
from engines.signature_db import SignatureDB
log = Log()

class CodeScanner:
    @staticmethod
    def scan(filepath=None, code=None):
        Anim.section("CODE THREAT ANALYSIS", "💻")

        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
                Anim.result("File", filepath[:55])
                Anim.result("Lines", str(code.count("\n") + 1))
                Anim.result("Size", str(len(code)) + " chars")
            except Exception as e:
                Anim.threat("ERROR", str(e)[:50])
                Anim.section_end()
                return None
        elif not code:
            Anim.threat("ERROR", "No code provided")
            Anim.section_end()
            return None

        results = {"threats": [], "stats": {}}

        # Run all signature checks
        Anim.scan_line("Malware Patterns", "\033[33mscanning...\033[0m", "🦠")
        findings = SignatureDB.scan_code(code)

        for f in findings:
            results["threats"].append(f)
            Anim.threat(f["severity"], f["description"] + " (" + str(f["matches"]) + " matches)")

        # Code statistics
        Anim.scan_line("Code Analysis", "\033[33manalyzing...\033[0m", "📊")
        dangerous_funcs = ["eval", "exec", "system", "popen", "shell_exec",
                           "passthru", "proc_open", "pcntl_exec", "assert"]
        for func in dangerous_funcs:
            count = code.lower().count(func + "(") + code.lower().count(func + " (")
            if count > 0:
                Anim.result("⚠️ " + func + "()", str(count) + " calls", Fore.RED)
                results["stats"][func] = count

        # Obfuscation indicators
        Anim.scan_line("Obfuscation", "\033[33mchecking...\033[0m", "🔮")
        obf_indicators = {
            "base64 strings": code.count("base64_decode") + code.count("atob(") + code.count("btoa("),
            "hex encoding": len([m for m in code.split("\\x") if len(m) > 1]) if "\\x" in code else 0,
            "unicode escapes": code.count("\\u00"),
            "eval() calls": code.count("eval("),
            "document.write": code.count("document.write"),
        }
        for name, count in obf_indicators.items():
            if count > 0:
                Anim.result("🔮 " + name, str(count), Fore.YELLOW)

        # Verdict
        crit = len([t for t in results["threats"] if t["severity"] == "CRITICAL"])
        high = len([t for t in results["threats"] if t["severity"] == "HIGH"])
        if crit > 0:
            Anim.threat("MALICIOUS", str(crit) + " critical findings - LIKELY MALWARE!")
        elif high > 0:
            Anim.threat("SUSPICIOUS", str(high) + " high severity findings")
        elif results["threats"]:
            Anim.threat("WARNING", str(len(results["threats"])) + " low/medium findings")
        else:
            Anim.threat("CLEAN", "No malicious patterns detected")

        Anim.section_end()
        return results

from colorama import Fore
