from dataclasses import dataclass


@dataclass(frozen=True)
class PageContent:
    page_number: int
    text: str
    char_count: int

    def __post_init__(self) -> None:
        if self.page_number < 1:
            raise ValueError("page_number must be 1-based and positive.")


@dataclass(frozen=True)
class ExtractedDocument:
    document_id: str
    filename: str
    total_pages: int
    pages: list[PageContent]

    @property
    def full_text(self) -> str:
        return "\n\n".join(
            f"[Page {page.page_number}]\n{page.text}"
            for page in self.pages
            if page.text
        )
