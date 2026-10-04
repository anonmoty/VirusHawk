import random, requests
from core.config import Config
from core.proxy import proxy
import urllib3
urllib3.disable_warnings()

class Session:
    def __init__(self):
        self.s = requests.Session()
        self.s.verify = False
        self.s.headers.update({"User-Agent": random.choice(Config.UAS), "Accept": "*/*", "Connection": "close"})

    def get(self, url, **kw):
        kw.setdefault("timeout", Config.TIMEOUT)
        kw["proxies"] = proxy.get()
        kw["verify"] = False
        if random.random() < 0.2: self.s.headers["User-Agent"] = random.choice(Config.UAS)
        try: return self.s.get(url, **kw)
        except:
            if kw.get("proxies"):
                proxy.kill(); kw.pop("proxies", None)
                try: return self.s.get(url, **kw)
                except: return None
            return None

    def post(self, url, **kw):
        kw.setdefault("timeout", Config.TIMEOUT)
        kw["proxies"] = proxy.get(); kw["verify"] = False
        try: return self.s.post(url, **kw)
        except: return None

http = Session()
