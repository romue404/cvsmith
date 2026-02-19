"""Command-line interface for CVSmith"""

from pathlib import Path
import click
from cvsmith.parser import load_yaml
from cvsmith.generator import CVGenerator

@click.command()
@click.option(
    '--yaml',
    type=click.Path(exists=True),
    required=True,
    help='Path to YAML CV file'
)
@click.option(
    '--template',
    type=str,
    required=True,
    help='Template name (e.g., modern.jinja2)',
    default="modern.jinja2"
)
@click.option(
    '--output',
    type=click.Path(),
    required=True,
    help='Output folder path (CV files will be saved as cv.pdf and cv.html)'
)
@click.option(
    '--paper-size',
    type=click.Choice(['a4', 'letter'], case_sensitive=False),
    default='a4',
    show_default=True,
    help='Paper size: a4 or letter'
)
def main(yaml, template, output, paper_size):
    """Generate a CV PDF and HTML from YAML data and a template."""
    try:
        # Load YAML data
        data = load_yaml(yaml)

        # Get templates directory
        templates_dir = Path(__file__).resolve().parent.parent.parent / 'templates'

        # Ensure output directory exists
        output_dir = Path(output).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Define output paths
        pdf_path = output_dir / 'cv.pdf'
        html_path = output_dir / 'cv.html'
        base_url = output_dir.as_uri()

        # Generate PDF and HTML
        generator = CVGenerator(str(templates_dir))
        html_content = generator.render_html(template, data, paper_size=paper_size)
        generator.generate_pdf(html_content, str(pdf_path), base_url=base_url, paper_size=paper_size)

        click.echo(f"✓ CV generated: {pdf_path}")

        # Save HTML
        html_path.write_text(html_content, encoding='utf-8')
        click.echo(f"✓ HTML exported: {html_path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise


if __name__ == '__main__':
    main()
