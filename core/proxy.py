import random, threading, requests
from core.config import Config
from core.logger import Log
log = Log()

class Proxy:
    def __init__(self):
        self.pool=[]; self.alive=[]; self.current=None
        self.count=0; self.dead=set(); self.lock=threading.Lock(); self.on=False

    def fetch(self):
        log.info("Fetching proxies from ProxyScrape...")
        for url in Config.PROXY_URLS:
            try:
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    px = [p.strip() for p in r.text.strip().split("\n") if ":" in p.strip()]
                    self.pool.extend(px)
            except: pass
        self.pool = list(set(self.pool))
        random.shuffle(self.pool)
        if self.pool: self._check()
        else: self.on = False

    def _check(self, n=15):
        self.alive = []
        from core.animator import Anim
        for i, p in enumerate(self.pool[:n]):
            Anim.progress(i+1, min(n, len(self.pool)), "Test " + p[:18])
            try:
                r = requests.get("http://httpbin.org/ip", proxies=self._f(p), timeout=5)
                if r.status_code == 200: self.alive.append(p)
            except: pass
        if self.alive:
            self.current = random.choice(self.alive)
            self.on = True
            log.ok("Proxy: " + self.current)
        else: self.on = False

    def _f(self, p):
        if not p.startswith(("http://","socks")): p = "http://" + p
        return {"http": p, "https": p}

    def get(self):
        if not self.on or not self.alive: return None
        with self.lock:
            self.count += 1
            if self.count % Config.PROXY_ROTATE == 0:
                avail = [p for p in self.alive if p != self.current and p not in self.dead]
                if avail: self.current = random.choice(avail)
            return self._f(self.current) if self.current else None

    def kill(self):
        if self.current:
            self.dead.add(self.current)
            if self.current in self.alive: self.alive.remove(self.current)
            avail = [p for p in self.alive if p not in self.dead]
            if avail: self.current = random.choice(avail)

proxy = Proxy()
