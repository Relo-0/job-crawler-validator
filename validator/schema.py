job_schema = {
    "type": "object",
    "properties": {
        "jobName": {"type": "string"},
        "custName": {"type": "string"},
        "salaryDesc": {"type": ["string", "null"]},
        "jobAddrNoDesc": {"type": ["string", "null"]},
        "link": {"type": "string"}
    },
    "required": ["jobName", "custName", "link"]
}
