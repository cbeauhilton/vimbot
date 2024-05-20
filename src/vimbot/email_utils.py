import re
from postmarker.core import PostmarkClient
from .config import POSTMARK_API_KEY, FROM_EMAIL

# Initialize Postmark client with your API key
postmark = PostmarkClient(server_token=POSTMARK_API_KEY)


def scan_for_email(text: str) -> str | None:
    """Scan the text for email addresses using regular expressions."""
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(email_regex, text)
    if match:
        return match.group()
    return None


def send_email(to: str, subject: str, body: str) -> None:
    """Send an email using Postmark."""
    postmark.emails.send(
        From=FROM_EMAIL,
        To=to,
        Subject=subject,
        HtmlBody=body,
    )


def process_query_and_response(query: str, response: str) -> None:
    """Process the query and response, scan for email, and send an email if found."""
    email = scan_for_email(query)
    if email:
        subject = "VimBot Query and Response"
        body = f"<h1>Query:</h1><p>{query}</p><h1>Response:</h1>{response}"
        send_email(email, subject, body)
