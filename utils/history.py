import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

class HistoryManager:
    @staticmethod
    def save(expression, result, status="success"):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expression": expression,
            "result": str(result),
            "status": status
        }
        
        data = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        
        data.append(entry)
        
        with open(HISTORY_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load():
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []