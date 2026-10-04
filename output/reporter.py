import json
from datetime import datetime
from core.config import Config

class Reporter:
    @staticmethod
    def save(name, data):
        Config.init()
        path = Config.report_path(name, "json")
        with open(path, "w") as f:
            json.dump({"target": name, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "results": data}, f, indent=2, default=str)
        return path

    @staticmethod
    def save_txt(name, data):
        Config.init()
        path = Config.report_path(name, "txt")
        with open(path, "w") as f:
            f.write("VirusHawk v1.0 - Threat Report\n")
            f.write("Target: " + name + "\n")
            f.write("Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("=" * 60 + "\n\n")
            f.write(json.dumps(data, indent=2, default=str))
        return path
