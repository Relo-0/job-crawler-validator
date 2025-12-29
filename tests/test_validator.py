import json

from validator.validator import JobValidator


def test_validate_writes_report(monkeypatch, tmp_path):
    jobs = [
        {"jobNo": "1", "jobName": "OK", "custName": "C"},
        {"jobNo": "2", "custName": "Missing name"},
    ]

    monkeypatch.chdir(tmp_path)

    validator = JobValidator()
    valid, errors = validator.validate(jobs)

    assert valid == [jobs[0]]
    assert errors == [
        {"jobNo": "2", "field": "", "message": "'jobName' is a required property"}
    ]

    report_path = tmp_path / "output" / "validation_report.json"
    assert report_path.exists()
    saved_errors = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved_errors == errors
