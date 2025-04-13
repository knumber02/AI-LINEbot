import json
import threading

_config = None
_lock = threading.Lock()

def load_config():
    global _config
    with _lock:
        if _config is None:
            with open('/src/config.json') as f:
                _config = json.load(f)
    return _config

def get_config():
    if _config is None:
        return load_config()
    return _config 
