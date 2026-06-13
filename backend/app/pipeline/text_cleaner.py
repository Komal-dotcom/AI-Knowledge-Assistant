import re


def clean_text(text: str) -> str:
    """Normalize whitespace and remove control characters from extracted PDF text."""
    if not text:
        return ""

    cleaned = text.replace("\x00", "")
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)

    return cleaned.strip()
