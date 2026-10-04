import re

class SignatureDB:
    """Local malware/threat signature database"""

    # Malicious code patterns
    MALWARE_PATTERNS = [
        (r'eval\s*\(\s*base64_decode\s*\(', "PHP eval(base64) - Backdoor", "CRITICAL"),
        (r'eval\s*\(\s*\$_(GET|POST|REQUEST|COOKIE)', "PHP eval from input - RCE", "CRITICAL"),
        (r'assert\s*\(\s*\$_(GET|POST|REQUEST)', "PHP assert injection - RCE", "CRITICAL"),
        (r'system\s*\(\s*\$_(GET|POST|REQUEST)', "PHP system() from input - RCE", "CRITICAL"),
        (r'exec\s*\(\s*\$_(GET|POST|REQUEST)', "PHP exec() from input - RCE", "CRITICAL"),
        (r'passthru\s*\(\s*\$_(GET|POST|REQUEST)', "PHP passthru - RCE", "CRITICAL"),
        (r'shell_exec\s*\(\s*\$_(GET|POST|REQUEST)', "PHP shell_exec - RCE", "CRITICAL"),
        (r'popen\s*\(\s*\$_(GET|POST|REQUEST)', "PHP popen - RCE", "CRITICAL"),
        (r'proc_open\s*\(\s*\$_(GET|POST|REQUEST)', "PHP proc_open - RCE", "CRITICAL"),
        (r'pcntl_exec\s*\(', "PHP pcntl_exec - RCE", "CRITICAL"),
        (r'\$_(GET|POST|REQUEST)\s*\[\s*["\'].*["\']\s*\]\s*\(', "Dynamic function call from input", "CRITICAL"),
        (r'create_function\s*\(', "PHP create_function (deprecated/dangerous)", "HIGH"),
        (r'preg_replace\s*\(\s*["\'].*/e["\']', "PHP preg_replace /e modifier - RCE", "CRITICAL"),
        (r'Runtime\.getRuntime\(\)\.exec\(', "Java Runtime.exec - RCE", "CRITICAL"),
        (r'ProcessBuilder', "Java ProcessBuilder - potential RCE", "HIGH"),
        (r'__import__\s*\(\s*["\']os["\']\s*\)', "Python os import - potential RCE", "HIGH"),
        (r'subprocess\.(call|Popen|run)\s*\(', "Python subprocess - potential RCE", "MEDIUM"),
        (r'os\.system\s*\(', "Python os.system - potential RCE", "HIGH"),
        (r'os\.popen\s*\(', "Python os.popen - potential RCE", "HIGH"),
        (r'child_process', "Node.js child_process - potential RCE", "MEDIUM"),
        (r'require\s*\(\s*["\']child_process["\']\s*\)', "Node.js child_process import", "HIGH"),
    ]

    # Web shell signatures
    WEBSHELL_PATTERNS = [
        (r'(?:c99|r57|b374k|wso|filesman|an0n)', "Known web shell name detected", "CRITICAL"),
        (r'GIF89a.*<\?php', "PHP shell hidden in GIF", "CRITICAL"),
        (r'<\?php.*\b(?:system|exec|passthru|shell_exec)\b.*\$_', "Generic PHP web shell", "CRITICAL"),
        (r'base64_decode\s*\(\s*["\'][A-Za-z0-9+/=]{50,}', "Long base64 payload (obfuscated shell)", "CRITICAL"),
        (r'\\x[0-9a-f]{2}(\\x[0-9a-f]{2}){10,}', "Hex-encoded payload", "HIGH"),
        (r'chr\s*\(\s*\d+\s*\)\s*\.\s*chr\s*\(\s*\d+', "PHP chr() obfuscation", "HIGH"),
        (r'StrToBin|BinToStr|gzinflate|gzuncompress|str_rot13', "PHP deobfuscation chain", "HIGH"),
        (r'\$\{["\']_*(?:GET|POST|REQUEST|COOKIE)', "PHP variable variable from input", "CRITICAL"),
    ]

    # Phishing patterns
    PHISHING_PATTERNS = [
        (r'(?:login|signin|sign-in|verify|confirm|secure|update|account|banking|paypal|apple|google|microsoft|amazon).*(?:password|passwd|credential|ssn|social.security|credit.card|cvv|pin)', "Phishing keyword combination", "HIGH"),
        (r'<form[^>]*action\s*=\s*["\']https?://[^"\']*(?:bit\.ly|tinyurl|goo\.gl|t\.co|is\.gd)', "Form posting to URL shortener", "CRITICAL"),
        (r'document\.cookie', "JavaScript cookie access", "MEDIUM"),
        (r'window\.location\s*=\s*["\'](?:https?://)?(?:bit\.ly|tinyurl|goo\.gl)', "Redirect to shortener", "HIGH"),
        (r'atob\s*\(|btoa\s*\(', "Base64 encoding in JS (obfuscation)", "LOW"),
        (r'new\s+Image\(\)\.src\s*=.*document\.cookie', "Cookie exfiltration via image", "CRITICAL"),
        (r'fetch\s*\(.*document\.cookie', "Cookie exfiltration via fetch", "CRITICAL"),
        (r'XMLHttpRequest.*document\.cookie', "Cookie exfiltration via XHR", "CRITICAL"),
        (r'navigator\.clipboard\.readText', "Clipboard access", "MEDIUM"),
        (r'getUserMedia', "Camera/mic access", "MEDIUM"),
        (r'geolocation\.getCurrentPosition', "Geolocation access", "LOW"),
    ]

    # Suspicious URL patterns
    URL_PATTERNS = [
        (r'(?:paypal|apple|google|microsoft|amazon|facebook|instagram|netflix|bank|secure|login|verify|account|update|confirm)', "Brand impersonation keyword", "HIGH"),
        (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', "Raw IP address in URL", "MEDIUM"),
        (r'(?:bit\.ly|tinyurl|goo\.gl|t\.co|is\.gd|ow\.ly|buff\.ly)', "URL shortener", "MEDIUM"),
        (r'(?:\.tk|\.ml|\.ga|\.cf|\.gq|\.xyz|\.top|\.buzz|\.click|\.link|\.icu|\.cam)', "Suspicious TLD", "MEDIUM"),
        (r'@', "URL with @ symbol (credential/redirect trick)", "HIGH"),
        (r'(?:%[0-9a-f]{2}){5,}', "Heavy URL encoding (obfuscation)", "MEDIUM"),
        (r'(?:data:|javascript:|vbscript:)', "Dangerous URL scheme", "CRITICAL"),
        (r'(?:\.exe|\.bat|\.cmd|\.scr|\.pif|\.vbs|\.ps1|\.msi|\.dll)(?:\?|$)', "Executable file extension", "HIGH"),
        (r'(?:\.php\?.*=.*\.\./)', "Path traversal in PHP", "HIGH"),
    ]

    # Obfuscation patterns
    OBFUSCATION_PATTERNS = [
        (r'\\u[0-9a-f]{4}(\\u[0-9a-f]{4}){3,}', "Unicode escape obfuscation", "MEDIUM"),
        (r'String\.fromCharCode\s*\(', "JS fromCharCode obfuscation", "MEDIUM"),
        (r'eval\s*\(\s*unescape\s*\(', "JS eval(unescape()) obfuscation", "HIGH"),
        (r'eval\s*\(\s*String\.fromCharCode', "JS eval(fromCharCode) obfuscation", "HIGH"),
        (r'atob\s*\(.*eval', "JS base64 + eval chain", "HIGH"),
        (r'charCodeAt|fromCharCode', "Character code manipulation", "LOW"),
        (r'(?:\\x[0-9a-f]{2}){5,}', "Hex string obfuscation", "MEDIUM"),
        (r'pack\s*\(\s*["\']H\*', "PHP pack() obfuscation", "HIGH"),
        (r'gzinflate\s*\(\s*base64_decode', "PHP gzinflate+base64 chain", "HIGH"),
    ]

    @classmethod
    def scan_code(cls, code):
        """Scan code against all signature databases"""
        findings = []
        all_patterns = cls.MALWARE_PATTERNS + cls.WEBSHELL_PATTERNS + cls.PHISHING_PATTERNS + cls.OBFUSCATION_PATTERNS

        for pattern, desc, severity in all_patterns:
            try:
                matches = re.findall(pattern, code, re.IGNORECASE)
                if matches:
                    findings.append({
                        "pattern": pattern[:50],
                        "description": desc,
                        "severity": severity,
                        "matches": len(matches),
                    })
            except re.error:
                continue
        return findings

    @classmethod
    def scan_url_pattern(cls, url):
        """Scan URL for suspicious patterns"""
        findings = []
        for pattern, desc, severity in cls.URL_PATTERNS:
            try:
                if re.search(pattern, url, re.IGNORECASE):
                    findings.append({"description": desc, "severity": severity})
            except re.error:
                continue
        return findings
