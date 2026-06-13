from backend.app.pipeline.text_cleaner import clean_text


def test_clean_text_normalizes_line_endings():
    assert clean_text("Hello\r\nWorld") == "Hello\nWorld"


def test_clean_text_collapses_excessive_blank_lines():
    assert clean_text("Line one\n\n\n\nLine two") == "Line one\n\nLine two"


def test_clean_text_removes_null_bytes():
    assert clean_text("Hello\x00World") == "HelloWorld"


def test_clean_text_returns_empty_string_for_blank_input():
    assert clean_text("   \n\n  ") == ""
