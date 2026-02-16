"""Command-line interface for CVSmith"""

import os
import click
from .parser import load_yaml
from .generator import CVGenerator


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
    help='Template name (e.g., modern.html)'
)
@click.option(
    '--output',
    type=click.Path(),
    required=True,
    help='Output PDF file path'
)
def main(yaml, template, output):
    """Generate a CV PDF from YAML data and a template."""
    try:
        # Load YAML data
        data = load_yaml(yaml)

        # Get templates directory
        templates_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 'templates'
        )

        # Generate PDF
        generator = CVGenerator(templates_dir)
        html = generator.render_html(template, data)
        generator.generate_pdf(html, output)

        click.echo(f"✓ CV generated: {output}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise


if __name__ == '__main__':
    main()
