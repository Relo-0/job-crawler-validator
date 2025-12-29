from pathlib import Path

import pandas as pd

from analyzer.skill_analyzer import SkillAnalyzer


def test_skill_analyzer_generates_reports(monkeypatch, tmp_path):
    keyword_path = Path(__file__).resolve().parents[1] / "config" / "skills_keywords.json"

    jobs = [
        {"description": "Python selenium and git", "company": "A", "salary_low": 50000},
        {"description": "python api testing git", "company": "B", "salary_low": 60000},
        {"description": "python automation ui selenium git", "company": "A", "salary_low": 70000},
    ]

    monkeypatch.chdir(tmp_path)

    analyzer = SkillAnalyzer(keyword_path=str(keyword_path))
    analyzer.analyze(jobs)

    reports_dir = tmp_path / "reports"
    assert (reports_dir / "skill_frequency.csv").exists()
    assert (reports_dir / "category_coverage.csv").exists()
    assert (reports_dir / "company_maturity.csv").exists()
    assert (reports_dir / "skill_salary_low.csv").exists()

    skill_freq = pd.read_csv(reports_dir / "skill_frequency.csv")
    python_row = skill_freq.loc[skill_freq["skill"] == "python"].iloc[0]
    assert python_row["count"] == 3
    assert python_row["ratio"] == 1.0

    salary_df = pd.read_csv(reports_dir / "skill_salary_low.csv")
    python_salary = salary_df.loc[salary_df["skill"] == "python"].iloc[0]
    assert python_salary["median_salary_low"] == 60000
    assert python_salary["count"] == 3

    company_df = pd.read_csv(reports_dir / "company_maturity.csv")
    company_a = company_df.loc[company_df["company"] == "A"].iloc[0]
    assert company_a["engineering"] == 2
