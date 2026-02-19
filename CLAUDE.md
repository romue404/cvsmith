# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CVSmith is a Python library that converts YAML-formatted CV data to professional PDF documents. It uses Jinja2 for HTML templating and Playwright for PDF generation. The project uses `uv` as the package manager.

## Development Commands

### Setup
```bash
uv sync                    # Install all dependencies
uv sync --all-extras       # Install including dev dependencies (pytest, black)
```

### Running
```bash
uv run cvsmith --yaml <yaml-file> --template <template-name> --output <pdf-file>
uv run cvsmith --yaml example.yaml --template modern.jinja2 --output cv.pdf
uv run cvsmith --yaml example.yaml --template modern.jinja2 --output cv.pdf --html cv.html  # Also save rendered HTML
uv run cvsmith --yaml "examples/assets/sherlock.yaml" --template "modern.jinja2" --output "examples/sherlock.pdf" --html "examples/sherlock.html"  # Sherlock Holmes example
uv run cvsmith --yaml example.yaml --template modern.jinja2 --output cv.pdf --paper-size letter  # Generate US Letter size
```

### Testing & Linting
```bash
uv run pytest              # Run all tests
uv run pytest tests/       # Run tests in specific directory
uv run pytest -xvs tests/test_name.py::test_function  # Run single test with output
uv run black src/          # Format code with black
```

## Architecture

The library follows a three-stage pipeline:

1. **Parser** (`src/cvsmith/parser.py`): Loads and validates YAML CV data
2. **Generator** (`src/cvsmith/generator.py`): Renders HTML from Jinja2 templates + data, then converts to PDF using Playwright
3. **CLI** (`src/cvsmith/cli.py`): Click-based command-line interface that orchestrates the pipeline

### Key Classes
- `CVGenerator`: Main class that manages Jinja2 environment and handles HTML→PDF conversion

### Template System
- Templates live in `templates/` directory with `.jinja2` extension
- Use Jinja2 syntax with standard CV sections (name, email, experience, education, skills, etc.)
- `modern.jinja2` provides A4 (default) or US Letter output with responsive styling
- Template variables come directly from YAML data structure
- Paper size can be controlled via `--paper-size` CLI flag (a4 or letter)

### Data Flow
YAML file → `load_yaml()` → dict → `CVGenerator.render_html()` → HTML string → `CVGenerator.generate_pdf()` → PDF file

## Common Tasks

**Adding a new template:** Create `.jinja2` file in `templates/` directory using Jinja2 syntax. Reference example variables in `example.yaml`. For paper size support, use `{{ page_css_size }}` and `{{ page_width }}` variables.

**Extending CV sections:** Modify `example.yaml` to add new data fields, then update templates to use them via `{{ field_name }}` syntax.

**Customizing personal info items:** Use the flexible `personal_info.info` list in YAML to define info items with unicode icons. Each item is rendered as a non-wrappable info piece. Example:
```yaml
personal_info:
  info:
    - "◆ PhD in Computer Science"
    - "⌂ New York, USA"
    - "☎ +1 (555) 1234"
    - "✉ email@example.com"
    - "◉ github.com/username"
```
The template automatically prevents text wrapping within each info piece using `white-space: nowrap`. The divider line below the header fades out on both sides and covers 75% of the width.

**Handling template errors:** Playwright PDF generation can be strict about HTML/CSS. Use `--html` flag to save rendered HTML and inspect it for structure issues. Common issues: unclosed tags, invalid CSS properties, or unsupported HTML elements. Check the generated HTML file first before debugging PDF output.

## Dependencies

- **Jinja2** (3.1.6): HTML templating
- **PyYAML** (6.0.3): YAML parsing
- **WeasyPrint** (68.1): HTML to PDF conversion
- **Click** (8.3.1): CLI framework
- **Playwright** (1.48.2): Browser automation for PDF generation
- **pytest** (dev): Testing framework
- **black** (dev): Code formatter

Python 3.13+
