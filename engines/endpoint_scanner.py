import re
from core.session import http
from core.animator import Anim
from core.logger import Log
from engines.signature_db import SignatureDB
log = Log()

class EndpointScanner:
    SUSPICIOUS_ENDPOINTS = [
        "/admin", "/login", "/wp-login.php", "/wp-admin",
        "/phpmyadmin", "/pma", "/server-status", "/server-info",
        "/.env", "/.git/HEAD", "/.git/config", "/.svn/entries",
        "/config.php", "/wp-config.php", "/database.yml",
        "/api/v1/users", "/api/admin", "/api/config",
        "/debug", "/__debug__/", "/actuator", "/actuator/env",
        "/swagger-ui.html", "/api-docs", "/graphql", "/graphiql",
        "/console", "/jmx-console", "/web-console",
        "/elmah.axd", "/trace.axd", "/telescope",
        "/backup", "/backup.sql", "/dump.sql", "/db.sql",
        "/shell.php", "/cmd.php", "/c99.php", "/r57.php",
        "/uploads/", "/upload.php", "/filemanager",
        "/xmlrpc.php", "/robots.txt", "/sitemap.xml",
        "/.htaccess", "/web.config", "/crossdomain.xml",
        "/phpinfo.php", "/info.php", "/test.php",
        "/cgi-bin/", "/.DS_Store", "/WEB-INF/web.xml",
    ]

    @classmethod
    def scan(cls, base_url):
        Anim.section("ENDPOINT THREAT SCAN", "🎯")
        base_url = base_url.rstrip("/")
        results = {"endpoints": [], "threats": []}

        total = len(cls.SUSPICIOUS_ENDPOINTS)
        for i, ep in enumerate(cls.SUSPICIOUS_ENDPOINTS):
            Anim.progress(i + 1, total, ep[:30])
            url = base_url + ep
            r = http.get(url, timeout=8, allow_redirects=False)
            if r:
                status = r.status_code
                size = len(r.text)
                if status in [200, 301, 302, 403]:
                    info = {"path": ep, "status": status, "size": size}

                    # Classify threat
                    threat_level = "INFO"
                    if ep in ["/.env", "/.git/HEAD", "/backup.sql", "/dump.sql",
                              "/shell.php", "/c99.php", "/r57.php", "/cmd.php"]:
                        if status == 200 and "404" not in r.text.lower()[:100]:
                            threat_level = "CRITICAL"
                    elif ep in ["/phpmyadmin", "/server-status", "/actuator/env",
                                "/.git/config", "/wp-config.php"]:
                        if status == 200:
                            threat_level = "HIGH"
                    elif status == 403:
                        threat_level = "WARNING"

                    info["threat"] = threat_level
                    results["endpoints"].append(info)

                    if threat_level in ["CRITICAL", "HIGH"]:
                        Anim.threat(threat_level, ep + " [HTTP " + str(status) + "]")
                        results["threats"].append({"description": "Exposed: " + ep, "severity": threat_level})
                    elif threat_level == "WARNING":
                        Anim.result("⚠️ " + ep, "HTTP 403 (exists but blocked)", Fore.YELLOW)
                    else:
                        Anim.result("  " + ep, "HTTP " + str(status), Fore.LIGHTBLACK_EX)

                    # Scan response for malicious content
                    if status == 200 and size > 10:
                        code_findings = SignatureDB.scan_code(r.text[:20000])
                        for f in code_findings:
                            results["threats"].append(f)
                            Anim.threat(f["severity"], ep + ": " + f["description"])

        # Summary
        crit = len([e for e in results["endpoints"] if e.get("threat") == "CRITICAL"])
        high = len([e for e in results["endpoints"] if e.get("threat") == "HIGH"])
        Anim.result("Total Found", str(len(results["endpoints"])))
        Anim.result("Critical", str(crit), Fore.RED)
        Anim.result("High", str(high), Fore.LIGHTRED_EX)

        Anim.section_end()
        return results

from colorama import Fore
