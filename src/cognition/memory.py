import json
import os

class Memory:
    def __init__(self, storage_file="src/cognition/notified_ids.json"):
        self.storage_file = storage_file
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        self.notified_ids = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"issues": [], "pull_requests": [], "commits": []}
        return {"issues": [], "pull_requests": [], "commits": []}

    def is_new(self, category, item_id):
        return item_id not in self.notified_ids.get(category, [])

    def save_id(self, category, item_id):
        if category not in self.notified_ids:
            self.notified_ids[category] = []
        if item_id not in self.notified_ids[category]:
            self.notified_ids[category].append(item_id)
            with open(self.storage_file, 'w') as f:
                json.dump(self.notified_ids, f, indent=4)

