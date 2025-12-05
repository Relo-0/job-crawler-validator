import json
from jsonschema import validate, ValidationError
from utils.logger import logger
from .schema import job_schema

class JobValidator:
    def validate(self, jobs: list):
        errors = []

        for item in jobs:
            try:
                validate(instance=item, schema=job_schema)
            except ValidationError as e:
                errors.append(str(e))

        # 輸出報告
        with open("output/validation_report.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)

        logger.info(f"驗證完成：{len(errors)} 個錯誤")
        return errors
