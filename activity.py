import datetime
import os

class ActivityLogger:
    def __init__(self, log_file="data/activity_log.txt"):
        self.log_file = log_file
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        directory = os.path.dirname(self.log_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def log(self, action, before, after):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] Action: {action} | Before: {before} | After: {after}\n"
        
        with open(self.log_file, "a") as f:
            f.write(entry)
