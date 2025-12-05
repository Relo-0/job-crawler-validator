def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return s.strip()
