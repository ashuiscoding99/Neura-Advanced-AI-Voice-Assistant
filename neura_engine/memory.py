import json
import os
from neura_engine.config import MEMORY_FILE

memory_store = {"facts": {}, "numbers": {}, "tasks": []}

def load_memory():
    global memory_store
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory_store = json.load(f)

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_store, f, indent=4)