"""Command-line interface for CVSmith"""

import os
from pathlib import Path
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
@click.option(
    '--html',
    type=click.Path(),
    required=False,
    help='Optional: Save rendered HTML to this file path'
)
@click.option(
    '--paper-size',
    type=click.Choice(['a4', 'letter'], case_sensitive=False),
    default='a4',
    show_default=True,
    help='Paper size: a4 or letter'
)
def main(yaml, template, output, html, paper_size):
    """Generate a CV PDF from YAML data and a template."""
    try:
        # Load YAML data
        data = load_yaml(yaml)

        # Get templates directory
        templates_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 'templates'
        )

        # Compute base URL from output PDF directory for resolving relative asset paths
        output_dir = Path(output).resolve().parent
        base_url = output_dir.as_uri()

        # Generate PDF
        generator = CVGenerator(templates_dir)
        html_content = generator.render_html(template, data, paper_size=paper_size)
        generator.generate_pdf(html_content, output, base_url=base_url, paper_size=paper_size)

        click.echo(f"✓ CV generated: {output}")

        # Optionally save HTML
        if html:
            with open(html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            click.echo(f"✓ HTML exported: {html}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise


if __name__ == '__main__':
    main()
