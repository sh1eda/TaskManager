import json
import os

class Storage:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_data(self, data):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
