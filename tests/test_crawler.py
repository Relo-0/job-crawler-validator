import json

from crawler.job_crawler import JobCrawler


def test_fetch_jobs_deduplicates_and_writes(monkeypatch, tmp_path):
    # Arrange: mock HttpClient responses across pages
    responses = [
        {
            "data": {
                "list": [
                    {"jobNo": "A1", "jobName": "Test 1", "custName": "C1"},
                    {"jobNo": "A1", "jobName": "Duplicate", "custName": "C1"},
                ]
            }
        },
        {"data": {"list": [{"jobNo": "B2", "jobName": "Test 2", "custName": "C2"}]}},
        {"data": {"list": []}},
    ]

    class FakeHttpClient:
        def get(self, url, headers=None, params=None, retries=3, delay=1):
            return responses.pop(0)

    monkeypatch.setattr("crawler.job_crawler.HttpClient", lambda: FakeHttpClient())
    monkeypatch.chdir(tmp_path)

    crawler = JobCrawler()

    # Act
    jobs = crawler.fetch_jobs(keyword="k", area="a", max_pages=3)

    # Assert: deduplication keeps unique jobNo entries and writes payload to disk
    assert jobs == [
        {"jobNo": "A1", "jobName": "Test 1", "custName": "C1"},
        {"jobNo": "B2", "jobName": "Test 2", "custName": "C2"},
    ]

    payload_path = tmp_path / "output" / "jobs_raw.json"
    assert payload_path.exists()

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    assert payload["meta"]["count"] == 2
    assert payload["jobs"] == jobs
