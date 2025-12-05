import json
from utils.http_client import HttpClient
from utils.logger import logger

class JobCrawler:
    BASE_URL = "https://www.104.com.tw/jobs/search/list"

    def fetch_jobs(self, keyword: str, area: str):
        params = {
            "keyword": keyword,
            "page": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.104.com.tw/jobs/search/"
        }

        http = HttpClient()
        data = http.get(self.BASE_URL, headers=headers, params=params)

        jobs = data.get("data", {}).get("list", [])

        # 輸出原始 JSON
        with open("output/jobs_raw.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)

        logger.info(f"取得 {len(jobs)} 筆職缺")
        return jobs
