from html.parser import HTMLParser
from typing import override
import mistune


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.modified_html: list[str] = []

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            attrs.append(("target", "_blank"))
        attrs_str = " ".join(f'{attr}="{val}"' for attr, val in attrs)
        self.modified_html.append(f"<{tag} {attrs_str}>")

    @override
    def handle_endtag(self, tag: str) -> None:
        self.modified_html.append(f"</{tag}>")

    @override
    def handle_data(self, data: str) -> None:
        self.modified_html.append(data)

    def get_modified_html(self) -> str:
        return "".join(self.modified_html)


def add_target_blank(html: str) -> str:
    """Add target="_blank" to all links in the HTML."""
    parser = LinkParser()
    parser.feed(html)
    return parser.get_modified_html()


def process_markdown(text: str) -> str:
    """Convert markdown to HTML using mistune."""
    html = mistune.html(text)
    return html


html = """
<ul>
<li>American Society of Hematology. (2020). Anemia. <a href="https://www.hematology.org/Patients/Anemia.aspx">https://www.hematology.org/Patients/Anemia.aspx</a></li>
<li>National Institute of Diabetes and Digestive and Kidney Diseases. (2020). Anemia. <a href="https://www.niddk.nih.gov/health-information/anemia">https://www.niddk.nih.gov/health-information/anemia</a></li>
</ul>
"""

if __name__ == "__main__":
    response = add_target_blank(html)
    print(response)
