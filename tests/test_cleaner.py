import json

from cleaner.cleaner import JobCleaner


def test_cleaner_transforms_and_parses_salary(monkeypatch, tmp_path):
    jobs = [
        {
            "jobNo": "A", "jobName": " Engineer ", "custName": " ACME ",
            "coIndustryDesc": "Software", "jobAddrNoDesc": "Taipei",
            "descWithoutHighlight": "testing automation", "salaryLow": "60000",
            "salaryHigh": "80000", "periodDesc": "2 years", "optionEdu": "BS",
            "link": {"job": "https://example.com/A"},
        },
        {"jobNo": "B", "jobName": None, "custName": None, "salaryLow": "n/a"},
    ]

    monkeypatch.chdir(tmp_path)
    (tmp_path / "output").mkdir()

    cleaner = JobCleaner()
    cleaned = cleaner.clean(jobs)

    assert cleaned[0]["job_id"] == "A"
    assert cleaned[0]["title"] == "Engineer"
    assert cleaned[0]["company"] == "ACME"
    assert cleaned[0]["salary_low"] == 60000
    assert cleaned[0]["salary_high"] == 80000
    assert cleaned[0]["url"] == "https://example.com/A"

    assert cleaned[1]["title"] == ""
    assert cleaned[1]["company"] == ""
    assert cleaned[1]["salary_low"] is None

    output_path = tmp_path / "output" / "jobs_clean.json"
    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved == cleaned
