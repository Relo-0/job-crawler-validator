import json
import os
from datetime import datetime
from utils.http_client import HttpClient
from utils.logger import logger

class JobCrawler:
    BASE_URL = "https://www.104.com.tw/jobs/search/list"

    def fetch_jobs(self, keyword: str, area: str, max_pages: int = 5):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.104.com.tw/jobs/search/"
        }

        http = HttpClient()
        all_jobs = []

        for page in range(1, max_pages + 1):
            params = {
                "keyword": keyword,
                "page": page,
                "area": area
            }

            data = http.get(self.BASE_URL, headers=headers, params=params)
            jobs = data.get("data", {}).get("list", [])

            if not jobs:
                break

            all_jobs.extend(jobs)
            logger.info(f"第 {page} 頁：{len(jobs)} 筆")

        # 去重
        seen = set()
        deduped = []
        for job in all_jobs:
            job_no = job.get("jobNo")
            if not job_no or job_no in seen:
                continue
            seen.add(job_no)
            deduped.append(job)

        os.makedirs("output", exist_ok=True)

        payload = {
            "meta": {
                "keyword": keyword,
                "area": area,
                "max_pages": max_pages,
                "count": len(deduped),
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "jobs": deduped
        }

        with open("output/jobs_raw.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        logger.info(f"取得 {len(deduped)} 筆職缺（已去重）")
        return deduped
