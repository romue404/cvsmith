"""HTML and PDF generation from CV data"""

import re
import tempfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


# Page size configuration for CSS rendering
_PAGE_VARS = {
    'a4':     {'page_css_size': 'A4',     'page_width': '210mm'},
    'letter': {'page_css_size': 'letter', 'page_width': '216mm'},
}


def linkify_info(text: str) -> str:
    """Convert emails, phone numbers, and URLs in text to clickable links while preserving icons."""
    # Keep the icon prefix and the rest
    icon_match = re.match(r'^([^\w\s]+)\s+(.+)$', text)
    if not icon_match:
        return text

    icon, content = icon_match.groups()

    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, content):
        email = re.search(email_pattern, content).group()
        content = f'<a href="mailto:{email}" class="cv-link">{email}</a>'

    # Phone pattern (e.g., +44 (0) 20 7946 0958, +1-234-567-8900)
    phone_pattern = r'(\+\d{1,3}[\s()\-.]?\d[\d\s()\-.]{5,})'
    if re.search(phone_pattern, content):
        phone_match = re.search(phone_pattern, content)
        phone = phone_match.group(1)
        # Create tel link with digits only
        phone_digits = re.sub(r'[^\d+]', '', phone)
        content = re.sub(
            re.escape(phone),
            f'<a href="tel:{phone_digits}" class="cv-link">{phone}</a>',
            content
        )

    # URL pattern (with or without http/https)
    url_pattern = r'(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    if re.search(url_pattern, content) and '@' not in content:  # Avoid matching emails
        url_match = re.search(url_pattern, content)
        url_text = url_match.group()
        url_href = url_text if url_text.startswith('http') else f'https://{url_text}'
        content = re.sub(
            re.escape(url_text),
            f'<a href="{url_href}" class="cv-link">{url_text}</a>',
            content
        )

    return f'{icon} {content}'


class CVGenerator:
    """Generate CV HTML and PDF from data and templates."""

    def __init__(self, templates_dir: str):
        """Initialize with templates directory."""
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.env.filters['linkify'] = linkify_info

    def render_html(self, template_name: str, data: dict, paper_size: str = 'a4') -> str:
        """Render HTML from template and data."""
        template = self.env.get_template(template_name)
        page_vars = _PAGE_VARS.get(paper_size.lower(), _PAGE_VARS['a4'])
        return template.render(**data, paper_size=paper_size, **page_vars)

    def generate_pdf(self, html_content: str, output_path: str, base_url: str | None = None, paper_size: str = 'a4') -> None:
        """Generate PDF from HTML content using Playwright."""
        # If base_url provided, write HTML to temp file in that directory so relative paths resolve
        html_file = None
        if base_url:
            # base_url is a file:// URL, extract the directory path
            base_path = Path(base_url.replace('file://', ''))
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', dir=base_path, delete=False, encoding='utf-8'
            ) as tmp:
                tmp.write(html_content)
                html_file = tmp.name

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                # Create page without viewport restriction so PDF pagination works correctly
                page = browser.new_page()

                if html_file:
                    # Navigate to the temp file so relative paths resolve from that directory
                    page.goto(f"file://{Path(html_file).resolve().as_posix()}", wait_until="networkidle")
                else:
                    # Fallback: set content directly if no base_url provided
                    page.set_content(html_content, wait_until="networkidle")

                page.emulate_media(media="print")
                _format_map = {'a4': 'A4', 'letter': 'Letter'}
                page.pdf(
                    path=str(Path(output_path)),
                    format=_format_map.get(paper_size.lower(), 'A4'),
                    print_background=True,
                    prefer_css_page_size=True,
                )

                browser.close()
        finally:
            # Clean up temp file if created
            if html_file:
                Path(html_file).unlink(missing_ok=True)
