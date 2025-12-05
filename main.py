from crawler.job_crawler import JobCrawler
from validator.validator import JobValidator
from cleaner.cleaner import JobCleaner
from analyzer.skill_analyzer import SkillAnalyzer

def main():
    # 1. 爬蟲：取得原始 JSON
    crawler = JobCrawler()
    raw_data = crawler.fetch_jobs(keyword="軟體測試", area="台北市")

    # 2. 驗證：以 Schema 檢查資料品質
    validator = JobValidator()
    validator.validate(raw_data)

    # 3. 清洗：統一欄位格式
    cleaner = JobCleaner()
    clean_data = cleaner.clean(raw_data)

    # 4. 分析：技能統計
    analyzer = SkillAnalyzer()
    analyzer.analyze(clean_data)

    print("流程完成：raw → validate → clean → analyze")

if __name__ == "__main__":
    main()
