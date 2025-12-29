job_schema = {
    "type": "object",
    "properties": {
        "jobNo": {"type": ["string", "null"]},
        "jobName": {"type": ["string", "null"]},
        "custName": {"type": ["string", "null"]},
        "jobAddrNoDesc": {"type": ["string", "null"]},
        "coIndustryDesc": {"type": ["string", "null"]},

        "descWithoutHighlight": {"type": ["string", "null"]},

        "salaryDesc": {"type": ["string", "null"]},
        "salaryLow": {"type": ["string", "null"]},
        "salaryHigh": {"type": ["string", "null"]},
        "salaryType": {"type": ["string", "null"]},

        "periodDesc": {"type": ["string", "null"]},
        "optionEdu": {"type": ["string", "null"]},
        "remoteWorkType": {"type": ["number", "null"]},

        "appearDate": {"type": ["string", "null"]},

        "link": {
            "type": ["object", "null"],
            "properties": {
                "job": {"type": ["string", "null"]},
                "cust": {"type": ["string", "null"]}
            }
        }
    },
    "required": ["jobNo", "jobName", "custName"]
}
