#!/usr/bin/env python3
"""VirusHawk - VirusTotal API v3 Client + Key Manager"""

import os
import time
import base64
from core.config import Config
from core.logger import Log

log = Log()


class VTClient:
    """VirusTotal API v3 Client with key management"""

    def __init__(self):
        self.key = Config.VT_API_KEY
        self.base = Config.VT_API_URL

    def _headers(self):
        return {"x-apikey": self.key}

    def available(self):
        return bool(self.key and len(self.key) > 20)

    def set_key(self, key):
        self.key = key
        Config.VT_API_KEY = key
        Config.save_key(key)

    def scan_url(self, url):
        if not self.available():
            return None
        from core.session import http
        try:
            r = http.post(self.base + "/urls",
                          data={"url": url},
                          headers=self._headers())
            if r and r.status_code == 200:
                return r.json().get("data", {}).get("id", "")
        except Exception as e:
            log.warn("VT URL scan error: " + str(e)[:50])
        return None

    def get_url_report(self, url):
        if not self.available():
            return None
        from core.session import http
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        try:
            r = http.get(self.base + "/urls/" + url_id, headers=self._headers())
            if r and r.status_code == 200:
                return r.json().get("data", {}).get("attributes", {})
        except Exception:
            pass
        return None

    def scan_file(self, filepath):
        if not self.available():
            return None
        from core.session import http
        try:
            with open(filepath, "rb") as f:
                r = http.post(self.base + "/files",
                              files={"file": f},
                              headers=self._headers())
                if r and r.status_code == 200:
                    return r.json().get("data", {}).get("id", "")
        except Exception as e:
            log.warn("VT file scan error: " + str(e)[:50])
        return None

    def get_file_report(self, file_hash):
        if not self.available():
            return None
        from core.session import http
        try:
            r = http.get(self.base + "/files/" + file_hash, headers=self._headers())
            if r and r.status_code == 200:
                return r.json().get("data", {}).get("attributes", {})
        except Exception:
            pass
        return None

    def get_ip_report(self, ip):
        if not self.available():
            return None
        from core.session import http
        try:
            r = http.get(self.base + "/ip_addresses/" + ip, headers=self._headers())
            if r and r.status_code == 200:
                return r.json().get("data", {}).get("attributes", {})
        except Exception:
            pass
        return None

    def get_domain_report(self, domain):
        if not self.available():
            return None
        from core.session import http
        try:
            r = http.get(self.base + "/domains/" + domain, headers=self._headers())
            if r and r.status_code == 200:
                return r.json().get("data", {}).get("attributes", {})
        except Exception:
            pass
        return None

    def parse_stats(self, attrs):
        if not attrs:
            return None
        stats = attrs.get("last_analysis_stats", {})
        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "timeout": stats.get("timeout", 0),
        }

    def parse_results(self, attrs):
        if not attrs:
            return []
        results = attrs.get("last_analysis_results", {})
        detections = []
        for engine, data in results.items():
            if data.get("category") in ["malicious", "suspicious"]:
                detections.append({
                    "engine": engine,
                    "result": data.get("result", ""),
                    "category": data.get("category", ""),
                })
        return detections


vt = VTClient()
