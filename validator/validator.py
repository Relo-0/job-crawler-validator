import json
import os
from jsonschema import validate, ValidationError
from utils.logger import logger
from .schema import job_schema

class JobValidator:
    def validate(self, jobs: list):
        os.makedirs("output", exist_ok=True)

        errors = []
        valid_jobs = []

        for item in jobs:
            try:
                validate(instance=item, schema=job_schema)
                valid_jobs.append(item)
            except ValidationError as e:
                errors.append({
                    "jobNo": item.get("jobNo"),
                    "field": "/".join([str(p) for p in e.path]),
                    "message": e.message
                })

        with open("output/validation_report.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)

        logger.info(f"驗證完成：{len(errors)} 個錯誤；通過：{len(valid_jobs)} 筆")
        return valid_jobs, errors
