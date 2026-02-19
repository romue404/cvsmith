# CVSmith

A modern Python library to convert YAML-formatted CV data to professional, clickable PDF documents using Jinja2 templates and Playwright.

## Preview

Here's what a CVSmith-generated CV looks like:

![Sherlock Holmes CV Preview](sherlock-preview.png)

## Features

- ✨ **Automatic Link Detection** - Email addresses, phone numbers, and URLs are automatically converted to clickable links in PDFs and HTML
- **Template-Based** - Highly customizable Jinja2 templates for professional CV design
- **Paper Size Control** - Generate A4 or US Letter format PDFs from the same data
- **Professional Output** - Clean, responsive HTML and PDF rendering using modern CSS
- **YAML-Powered** - Simple YAML format for CV content, easy to maintain and version control

## Installation

```bash
uv sync
```

## Quick Start

```bash
uv run cvsmith --yaml examples/sherlock.yaml --template modern.jinja2 --output cv.pdf
```

### Common Commands

Save HTML output alongside PDF:

```bash
uv run cvsmith --yaml examples/sherlock.yaml --template modern.jinja2 --output cv.pdf --html cv.html
```

Generate US Letter size:

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

## Creating Your CV

### Basic YAML Format

Create a `cv.yaml` file with your CV data. See the full [Sherlock Holmes example](examples/sherlock.yaml) for a complete structure.

Basic structure:

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

about_me: "Your professional summary..."

sections:
  - name: "EDUCATION"
    entries:
      - period: "2018 – 2022"
        title: "Degree Name"
        subtitle: "University Name"
        details:
          - "Achievement or skill"
        technologies: ["Skill1", "Skill2"]

skills:
  - category: "Languages"
    items:
      - skill: "Python"
        level: 5
```

**Flexible Sections**: You can omit any section entirely. No skills? Don't include the `skills` section. No photo? Leave `photo` empty or remove it. The template adapts to what you provide.

For a complete, real-world example with all sections, see [examples/sherlock.yaml](examples/sherlock.yaml).

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

Currently, CVSmith includes the **modern.jinja2** template, a professional CV design with:

- Clean typography and spacing
- Professional timeline-based layout
- Responsive design for both screen and print
- Support for nested positions (e.g., promotions within companies)
- Automatic link detection in contact info

The template uses standard Jinja2 syntax and has access to all your YAML data. You can customize colors, fonts, and layout by modifying the CSS variables in [templates/modern.jinja2](templates/modern.jinja2):

```jinja2
{% for section in sections %}
  <h2>{{ section.name }}</h2>
  {% for entry in section.entries %}
    <h3>{{ entry.title }}</h3>
    <!-- Entry details here -->
  {% endfor %}
{% endfor %}
```

## Testing & Development

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

## Project Info

- **Python**: 3.13+
- **Main Dependencies**: Jinja2, PyYAML, Playwright, Click
- **Built With**: Jinja2 (templating), Playwright (PDF generation), Click (CLI)

See [examples/](examples/) for working examples including the Sherlock Holmes CV.
