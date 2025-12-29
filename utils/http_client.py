import requests
import time

class HttpClient:
    def get(self, url, headers=None, params=None, retries=3, delay=1):
        last_err = None
        for attempt in range(1, retries + 1):
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_err = e
                if attempt == retries:
                    raise
                time.sleep(delay * attempt)  # 線性退避（簡單夠用）
        raise last_err
