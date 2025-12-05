import json
import pandas as pd

class SkillAnalyzer:
    def __init__(self):
        # 可從 config/skills_keywords.json 讀取
        self.keywords = self._load_keywords()

    def _load_keywords(self):
        try:
            with open("config/skills_keywords.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            # 預設最小技能集
            return ["python", "selenium", "api", "git", "linux", "sql"]

    def analyze(self, jobs: list):
        skills = []

        for job in jobs:
            desc = (job.get("title", "") + " " + job.get("company", "")).lower()
            matched = [k for k in self.keywords if k.lower() in desc]
            skills.extend(matched)

        df = pd.DataFrame(skills, columns=["skill"])
        summary = df["skill"].value_counts()

        summary.to_csv("reports/skills_summary.csv", encoding="utf-8")

        print("技能統計完成")
