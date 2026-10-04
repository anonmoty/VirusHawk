import os
from datetime import datetime

class Config:
    APP = "VirusHawk"
    VERSION = "1.0.0"
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS = os.path.join(BASE, "output")
    TIMEOUT = 15
    DELAY = 0.3
    PROXY_ROTATE = 8
    PROXY_URLS = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all",
    ]
    UAS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15",
    ]
    # VirusTotal API key (free: https://www.virustotal.com/gui/my-apikey)
    VT_API_KEY = ""
    VT_API_URL = "https://www.virustotal.com/api/v3"

    @classmethod
    def init(cls):
        os.makedirs(cls.REPORTS, exist_ok=True)
        key_file = os.path.join(cls.BASE, ".vt_key")
        if not cls.VT_API_KEY and os.path.exists(key_file):
            with open(key_file) as f:
                cls.VT_API_KEY = f.read().strip()

    @classmethod
    def save_key(cls, key):
        cls.VT_API_KEY = key
        with open(os.path.join(cls.BASE, ".vt_key"), "w") as f:
            f.write(key)

    @classmethod
    def report_path(cls, name, ext="txt"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = name.replace("/","_").replace(":","_").replace(".","_")[:30]
        return os.path.join(cls.REPORTS, "hawk_" + safe + "_" + ts + "." + ext)
