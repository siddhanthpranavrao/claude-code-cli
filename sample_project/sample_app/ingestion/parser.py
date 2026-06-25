import re


class MarkdownParser:
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    def extract_headings(self, text: str) -> list[str]:
        return [match.group(2).strip() for match in self.heading_pattern.finditer(text)]

    def normalize(self, text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

