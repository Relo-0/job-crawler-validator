import json
from utils.helpers import clean_text

class JobCleaner:
    def clean(self, jobs: list):
        cleaned = []

        for job in jobs:
            cleaned.append({
                # === 識別與分群 ===
                "job_id": job.get("jobNo"),
                "title": clean_text(job.get("jobNameRaw") or job.get("jobName")),
                "company": clean_text(job.get("custNameRaw") or job.get("custName")),
                "industry": clean_text(job.get("coIndustryDesc")),
                "location": clean_text(job.get("jobAddrNoDesc")),
                "posted_date": job.get("appearDate"),

                # === 分析核心 ===
                "description": clean_text(job.get("descWithoutHighlight")),

                # === 條件 / 市場判斷 ===
                "salary_low": self._parse_salary(job.get("salaryLow")),
                "salary_high": self._parse_salary(job.get("salaryHigh")),
                "experience": clean_text(job.get("periodDesc")),
                "education": clean_text(job.get("optionEdu")),

                # === 回溯用 ===
                "url": job.get("link", {}).get("job")
            })

        with open("output/jobs_clean.json", "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        return cleaned

    def _parse_salary(self, value):
        try:
            value = int(value)
            return value if value > 0 else None
        except:
            return None
