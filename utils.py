# utils.py
import json
from pathlib import Path

MEMORY_FILE = Path("arc_studio_v15.json")

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"designs": [], "logs": []}
