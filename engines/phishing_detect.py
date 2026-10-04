import re
from core.session import http
from core.animator import Anim
from core.logger import Log
from engines.signature_db import SignatureDB
log = Log()

class PhishingDetector:
    @staticmethod
    def scan(url):
        Anim.section("PHISHING DETECTION", "🎣")
        results = {"url": url, "threats": [], "score": 0}

        Anim.scan_line("URL Analysis", "\033[33mscanning...\033[0m", "🔬")

        # URL-based checks
        checks = [
            ("IP in URL", bool(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url)), 20),
            ("URL shortener", bool(re.search(r'bit\.ly|tinyurl|goo\.gl|t\.co', url, re.I)), 15),
            ("@ in URL", "@" in url, 25),
            ("Suspicious TLD", bool(re.search(r'\.(tk|ml|ga|cf|gq|xyz|top|buzz|click|icu|cam)$', url, re.I)), 15),
            ("HTTPS missing", not url.startswith("https"), 10),
            ("Long URL", len(url) > 150, 10),
            ("Many subdomains", url.count(".") > 3, 10),
            ("Brand + suspicious", bool(re.search(r'(paypal|apple|google|microsoft|amazon|facebook|netflix|bank).*(?:\.tk|\.ml|\.ga|\.xyz|\.top|\d+\.\d+)', url, re.I)), 30),
            ("data: URI", "data:" in url, 30),
            ("javascript: URI", "javascript:" in url, 30),
        ]

        for name, detected, points in checks:
            if detected:
                results["score"] += points
                results["threats"].append({"description": name, "severity": "HIGH" if points >= 20 else "MEDIUM"})
                Anim.threat("HIGH" if points >= 20 else "MEDIUM", name + " (+" + str(points) + " pts)")

        # Page content analysis
        Anim.scan_line("Page Content", "\033[33manalyzing...\033[0m", "📄")
        r = http.get(url)
        if r and r.status_code == 200:
            body = r.text.lower()

            # Check for login forms on suspicious domains
            has_login = bool(re.search(r'<input[^>]*type=["\']password["\']', body))
            has_brand = bool(re.search(r'(paypal|apple|google|microsoft|amazon|facebook|instagram|netflix)', body))
            if has_login and has_brand:
                results["score"] += 25
                Anim.threat("HIGH", "Login form with brand keywords (+25 pts)")

            # Check for urgency language
            urgency = ["immediately", "urgent", "suspend", "verify now", "24 hours", "limited time", "act now"]
            for word in urgency:
                if word in body:
                    results["score"] += 5
                    Anim.threat("MEDIUM", "Urgency language: '" + word + "'")
                    break

            # Code-based phishing patterns
            code_findings = SignatureDB.scan_code(r.text[:30000])
            for f in code_findings:
                if "phish" in f["description"].lower() or "cookie" in f["description"].lower() or "exfil" in f["description"].lower():
                    results["threats"].append(f)
                    Anim.threat(f["severity"], f["description"])

        # Final score
        print()
        if results["score"] >= 60:
            Anim.threat("MALICIOUS", "PHISHING SCORE: " + str(results["score"]) + "/100 🔴")
        elif results["score"] >= 30:
            Anim.threat("SUSPICIOUS", "PHISHING SCORE: " + str(results["score"]) + "/100 🟠")
        elif results["score"] >= 10:
            Anim.threat("WARNING", "PHISHING SCORE: " + str(results["score"]) + "/100 🟡")
        else:
            Anim.threat("CLEAN", "PHISHING SCORE: " + str(results["score"]) + "/100 🟢")

        Anim.section_end()
        return results
