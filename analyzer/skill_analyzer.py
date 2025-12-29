import json
import os
from collections import Counter, defaultdict
import pandas as pd


class SkillAnalyzer:
    def __init__(self, keyword_path="config/skills_keywords.json"):
        self.keywords = self._load_keywords(keyword_path)

    # ---------- utils ----------
    def _load_keywords(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _ensure_reports_dir(self):
        os.makedirs("reports", exist_ok=True)

    def _get_text(self, job):
        text = job.get("description") or ""
        return text.lower()

    # ---------- 1. 技能次數 & 覆蓋率 ----------
    def analyze_skill_frequency(self, jobs):
        total_jobs = len(jobs)
        skill_counter = Counter()

        for job in jobs:
            text = self._get_text(job)
            for category, skills in self.keywords.items():
                for skill in skills:
                    if skill in text:
                        skill_counter[skill] += 1

        rows = []
        for skill, count in skill_counter.items():
            rows.append({
                "skill": skill,
                "count": count,
                "ratio": round(count / total_jobs, 3)
            })

        df = pd.DataFrame(rows).sort_values("count", ascending=False)
        df.to_csv("reports/skill_frequency.csv", index=False, encoding="utf-8-sig")

    # ---------- 2. 技能分類覆蓋率 ----------
    def analyze_category_coverage(self, jobs):
        total_jobs = len(jobs)
        category_counter = Counter()

        for job in jobs:
            text = self._get_text(job)
            for category, skills in self.keywords.items():
                if any(skill in text for skill in skills):
                    category_counter[category] += 1

        rows = []
        for category, count in category_counter.items():
            rows.append({
                "category": category,
                "count": count,
                "ratio": round(count / total_jobs, 3)
            })

        df = pd.DataFrame(rows).sort_values("count", ascending=False)
        df.to_csv("reports/category_coverage.csv", index=False, encoding="utf-8-sig")

    # ---------- 3. 公司層級成熟度 ----------
    def analyze_company_maturity(self, jobs):
        company_stats = defaultdict(lambda: {
            "manual": 0,
            "hybrid": 0,
            "engineering": 0
        })

        for job in jobs:
            text = self._get_text(job)
            company = job.get("company")

            has_testing = any(
                skill in text for skill in self.keywords.get("testing_concepts", [])
            )
            has_automation = any(
                skill in text for skill in self.keywords.get("automation_ui", []) +
                                self.keywords.get("automation_api", [])
            )
            has_engineering = any(
                skill in text for skill in self.keywords.get("languages", []) +
                                self.keywords.get("tools_dev", [])
            )

            if has_engineering:
                maturity = "engineering"
            elif has_automation:
                maturity = "hybrid"
            else:
                maturity = "manual"

            company_stats[company][maturity] += 1

        rows = []
        for company, stats in company_stats.items():
            rows.append({
                "company": company,
                **stats
            })

        df = pd.DataFrame(rows).sort_values(
            ["engineering", "hybrid", "manual"], ascending=False
        )
        df.to_csv("reports/company_maturity.csv", index=False, encoding="utf-8-sig")

    # ---------- 4. 技能 × 薪資下限（安全版） ----------
    def analyze_skill_salary(self, jobs):
        salary_data = defaultdict(list)

        for job in jobs:
            salary = job.get("salary_low")
            if salary is None:
                continue

            text = self._get_text(job)
            for category, skills in self.keywords.items():
                for skill in skills:
                    if skill in text:
                        salary_data[skill].append(salary)

        rows = []
        for skill, salaries in salary_data.items():
            if len(salaries) < 3:
                continue  # 樣本太少不列

            rows.append({
                "skill": skill,
                "count": len(salaries),
                "median_salary_low": int(pd.Series(salaries).median()),
                "min_salary_low": min(salaries),
                "max_salary_low": max(salaries)
            })

        df = pd.DataFrame(rows).sort_values(
            "median_salary_low", ascending=False
        )
        df.to_csv("reports/skill_salary_low.csv", index=False, encoding="utf-8-sig")

    # ---------- main entry ----------
    def analyze(self, jobs):
        self._ensure_reports_dir()

        self.analyze_skill_frequency(jobs)
        self.analyze_category_coverage(jobs)
        self.analyze_company_maturity(jobs)
        self.analyze_skill_salary(jobs)

        print("Analyzer 完成：已產出 reports/*.csv")
