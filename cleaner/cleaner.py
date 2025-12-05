import json
from utils.helpers import clean_text

class JobCleaner:
    def clean(self, jobs: list):
        cleaned = []

        for job in jobs:
            cleaned.append({
                "title": clean_text(job.get("jobName")),
                "company": clean_text(job.get("custName")),
                "salary": clean_text(job.get("salaryDesc")),
                "location": clean_text(job.get("jobAddrNoDesc")),
                "url": job.get("link")
            })

        with open("output/jobs_clean.json", "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        return cleaned
