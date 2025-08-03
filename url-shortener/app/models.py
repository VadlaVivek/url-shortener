# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

# app/models.py
import threading
from datetime import datetime

class URLStore:
    def __init__(self):
        self.urls = {}
        self.lock = threading.Lock()

    def add(self, short_code, original_url):
        with self.lock:
            self.urls[short_code] = {
                "url": original_url,
                "created_at": datetime.utcnow(),
                "clicks": 0
            }

    def get(self, short_code):
        return self.urls.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.urls:
                self.urls[short_code]["clicks"] += 1
