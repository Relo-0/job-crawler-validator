# Job Crawler Validator

一個基於 **Python** 的 104 職缺蒐集與驗證工具，
自動完成「爬蟲 → schema 驗證 → 欄位清理 → 技能分析」全流程，並輸出 JSON / CSV 報表。

---

## 功能特點

- ✅ 自動呼叫 104 搜尋 API，處理分頁並去重
- ✅ 原始職缺資料輸出 `output/jobs_raw.json`
- ✅ 依 `jsonschema` 驗證欄位，錯誤列表輸出 `output/validation_report.json`
- ✅ 解析薪資與欄位正規化，輸出乾淨資料 `output/jobs_clean.json`
- ✅ 依 `config/skills_keywords.json` 進行技能頻率、分類覆蓋、公司成熟度、技能 × 薪資交叉分析
- ✅ 分析報表輸出 CSV（`reports/skill_frequency.csv` 等），自動建立目錄
- ✅ 支援讀取既有原始檔重跑（關閉爬蟲只做驗證/清理/分析）

---

## 專案結構

```
Job Crawler Validator/
├── main.py                   # 流程入口（預設抓「軟體測試」台北市 10 頁職缺）
├── requirements.txt          # 依賴套件
├── config/
│   └── skills_keywords.json  # 技能關鍵字設定
├── crawler/
│   └── job_crawler.py        # JobCrawler：呼叫 104 API、寫入 jobs_raw.json
├── validator/
│   ├── schema.py             # jsonschema 定義
│   └── validator.py          # JobValidator：驗證並輸出 validation_report.json
├── cleaner/
│   └── cleaner.py            # JobCleaner：欄位清理、薪資解析、產出 jobs_clean.json
├── analyzer/
│   └── skill_analyzer.py     # SkillAnalyzer：技能統計與報表輸出
├── utils/
│   ├── http_client.py        # HTTP 請求共用工具
│   ├── helpers.py            # 文字與欄位處理工具
│   └── logger.py             # 日誌工具
├── tests/                    # Pytest 測試
└── output/ & reports/        # 執行時自動建立的輸出資料夾
```

---

## 安裝步驟

### 1. Clone 專案

```bash
git clone <repo-url>
cd job-crawler-validator
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

> 建議 Python 3.10+；無需額外瀏覽器驅動，純 API 存取。

---

## 配置關鍵字與地區

- 預設在 `main.py` 呼叫 `crawler.fetch_jobs(keyword="軟體測試", area="台北市", max_pages=10)`。
- 若要調整技能分類或關鍵字，編輯 `config/skills_keywords.json` 後重新執行即可。

---

## 使用方法

### A. 直接抓取並跑完整流程

```bash
python main.py
```

會依參數抓取 104 職缺，依序完成驗證、清理、分析並產出報表。

### B. 讀取既有原始檔重跑（跳過爬蟲）

在 `main.py` 打開「模式 B」並註解模式 A：

```python
# payload = load_raw_payload()
# raw_jobs = payload.get("jobs", [])
```

此時流程會讀取 `output/jobs_raw.json` 直接做驗證、清理與分析。

---

## 輸出結果

- `output/jobs_raw.json`：原始職缺與 meta
- `output/validation_report.json`：欄位驗證錯誤列表
- `output/jobs_clean.json`：清理後的職缺資料
- `reports/skill_frequency.csv`：技能命中次數與覆蓋率
- `reports/category_coverage.csv`：技能分類覆蓋率
- `reports/company_maturity.csv`：公司成熟度分佈
- `reports/skill_salary_low.csv`：技能與薪資下限交叉統計（樣本 < 3 會被忽略）

---

## 已知限制

- 目前只使用 `main.py` 內設定的單一關鍵字與地區；未提供 CLI 參數
- 依賴 104 搜尋 API，若介面變動需調整 `crawler/job_crawler.py`
- 技能關鍵字統計取決於 `config/skills_keywords.json`，未做語意擴充
- 分析與輸出皆為 CSV/JSON，未內建視覺化

---

## 依賴套件

- requests
- jsonschema
- pandas
- pytest

完整清單請參考 `requirements.txt`
