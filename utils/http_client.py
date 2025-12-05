import requests
import time

class HttpClient:
    def get(self, url, headers=None, params=None, retries=3, delay=1):
        for attempt in range(retries):
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)
