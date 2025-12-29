import json
from crawler.job_crawler import JobCrawler
from validator.validator import JobValidator
from cleaner.cleaner import JobCleaner
from analyzer.skill_analyzer import SkillAnalyzer

def load_raw_payload(path="output/jobs_raw.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    crawler = JobCrawler()
    validator = JobValidator()
    cleaner = JobCleaner()
    analyzer = SkillAnalyzer()

    # 模式 A：直接抓（fetch_jobs 回傳 list，raw 檔案會寫 {meta, jobs}）
    raw_jobs = crawler.fetch_jobs(keyword="軟體測試", area="台北市", max_pages=10)

    # 模式 B：讀檔重跑（需要時再開）
    # payload = load_raw_payload()
    # raw_jobs = payload.get("jobs", [])

    valid_jobs, errors = validator.validate(raw_jobs)

    clean_data = cleaner.clean(valid_jobs)
    analyzer.analyze(clean_data)

    print("流程完成：raw → validate → clean → analyze")

if __name__ == "__main__":
    main()
