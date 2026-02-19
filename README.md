# CVSmith

A modern Python library to convert YAML-formatted CV data to professional, clickable PDF documents using Jinja2 templates and Playwright.

## Features

- ✨ **Automatic Link Detection** - Email addresses, phone numbers, and URLs are automatically converted to clickable links in PDFs and HTML
- **Template-Based** - Highly customizable Jinja2 templates for professional CV design
- **Paper Size Control** - Generate A4 or US Letter format PDFs from the same data
- **Professional Output** - Clean, responsive HTML and PDF rendering using modern CSS
- **YAML-Powered** - Simple YAML format for CV content, easy to maintain and version control

## Example

Here's what a CVSmith-generated CV looks like:

![Sherlock Holmes CV Preview](examples/sherlock-preview.png)

## Installation

```bash
uv sync
```

## Usage

### Basic Usage

```bash
uv run cvsmith --yaml examples/sherlock.yaml --template modern.jinja2 --output cv.pdf
```

### Save HTML Output

```bash
uv run cvsmith --yaml examples/sherlock.yaml --template modern.jinja2 --output cv.pdf --html cv.html
```

### Generate US Letter Size

```bash
uv run cvsmith --yaml examples/sherlock.yaml --template modern.jinja2 --output cv.pdf --paper-size letter
```

### Command-Line Options

```text
--yaml PATH            Path to YAML file with CV data (required)
--template NAME        Template filename in templates/ directory (required)
--output PATH          Output PDF file path (required)
--html PATH            Optional: also save rendered HTML file
--paper-size SIZE      Paper size: 'a4' (default) or 'letter'
```

## YAML Format

Create a `cv.yaml` file:

```yaml
name: Your Name
title: Your Professional Title
photo: path/to/photo.jpg

personal_info:
  info:
    - "◆ Born 01.01.1990"
    - "⌂ City, Country"
    - "☎ +1-234-567-8900"
    - "✉ your.email@example.com"
    - "◉ yourwebsite.com"

about_me: "Brief professional summary..."

sections:
  - name: "EDUCATION"
    entries:
      - period: "2018 – 2022"
        title: "Degree Name"
        subtitle: "University Name"
        details:
          - "Achievement or skill learned"
          - "Another accomplishment"
        technologies: ["Skill1", "Skill2"]

  - name: "CAREER"
    entries:
      - period: "2022 – present"
        title: "Job Title"
        subtitle: "Company Name"
        details:
          - "Key responsibility or achievement"
        technologies: ["Tech1", "Tech2"]
        positions:
          - period: "2023 – present"
            title: "Promoted to Senior Role"
            details:
              - "New responsibility"

skills:
  - category: "Languages"
    items:
      - skill: "Python"
        level: 5
      - skill: "JavaScript"
        level: 4
```

## Features in Detail

### Automatic Link Detection

The template automatically detects and creates clickable links for:

- **Emails**: `sherlock@bakerstreet.london` → `mailto:` link
- **Phone Numbers**: `+44 (0) 20 7946 0958` → `tel:` link
- **Websites**: `consulting-detective.co.uk` → `https://` link

Just add them to your `personal_info` section and they'll be clickable in PDFs!

### Paper Size Support

CVSmith generates PDFs optimized for:

- **A4** (default): 210mm × 297mm - Standard international format
- **Letter**: 216mm × 279mm - Standard US/Canada format

Use `--paper-size letter` to switch formats without changing your CV data.

### Customizable Templates

Templates use Jinja2 syntax and have access to all your YAML data:

```jinja2
{{ name }}
{{ about_me }}
{% for section in sections %}
  <h2>{{ section.name }}</h2>
  {% for entry in section.entries %}
    <h3>{{ entry.title }}</h3>
    <!-- Render entry details -->
  {% endfor %}
{% endfor %}
```

## Project Structure

```text
.
├── src/cvsmith/
│   ├── cli.py           # Command-line interface
│   ├── generator.py     # HTML/PDF generation logic
│   ├── parser.py        # YAML parsing
│   └── __init__.py
├── templates/
│   └── modern.jinja2    # Professional CV template
├── examples/
│   ├── sherlock.yaml    # Example CV data
│   ├── sherlock.html    # Rendered HTML
│   ├── sherlock.pdf     # Generated PDF
│   └── assets/          # Images for CVs
├── tests/               # Test suite
├── pyproject.toml       # Project configuration
└── README.md
```

## Development

### Setup

```bash
uv sync --all-extras
```

### Run Tests

```bash
uv run pytest
```

### Format Code

```bash
uv run black src/
```

### Run Single Test

```bash
uv run pytest -xvs tests/test_name.py::test_function
```

## Dependencies

- **Jinja2** (3.1.6) - HTML templating
- **PyYAML** (6.0.3) - YAML parsing
- **Playwright** (1.48.2) - Browser automation for PDF generation
- **Click** (8.3.1) - CLI framework
- **pytest** (dev) - Testing framework
- **black** (dev) - Code formatter

Requires Python 3.13+

## Examples

Check out `examples/` for complete working examples:

- `sherlock.yaml` - Full example with all sections
- `sherlock.html` - Rendered HTML output
- `sherlock.pdf` - Final PDF output

## Why CVSmith?

Traditional CV builders are either:

- **Too rigid** - Limited customization
- **Too complex** - Require web interfaces
- **Not version-controllable** - Data locked in databases

CVSmith enables:

- ✅ Full version control of your CV data
- ✅ Complete customization via templates
- ✅ Professional PDF output
- ✅ Simple YAML format (easy to read and edit)
- ✅ Automated testing of CV rendering

## License

MIT
