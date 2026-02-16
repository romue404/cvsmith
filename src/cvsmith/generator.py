"""HTML and PDF generation from CV data"""

import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io


class CVGenerator:
    """Generate CV HTML and PDF from data and templates."""

    def __init__(self, templates_dir: str):
        """Initialize with templates directory."""
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def render_html(self, template_name: str, data: dict) -> str:
        """Render HTML from template and data."""
        template = self.env.get_template(template_name)
        return template.render(**data)

    def generate_pdf(self, html_content: str, output_path: str) -> None:
        """Generate PDF from HTML content."""
        HTML(string=html_content).write_pdf(output_path)
