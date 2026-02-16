# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CVSmith is a Python library that converts YAML-formatted CV data to professional PDF documents. It uses Jinja2 for HTML templating and WeasyPrint for PDF generation. The project uses `uv` as the package manager.

## Development Commands

### Setup
```bash
uv sync                    # Install all dependencies
uv sync --all-extras       # Install including dev dependencies (pytest, black)
```

### Running
```bash
uv run cvsmith --yaml <yaml-file> --template <template-name> --output <pdf-file>
uv run cvsmith --yaml example.yaml --template modern.html --output cv.pdf
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
2. **Generator** (`src/cvsmith/generator.py`): Renders HTML from Jinja2 templates + data, then converts to PDF
3. **CLI** (`src/cvsmith/cli.py`): Click-based command-line interface that orchestrates the pipeline

### Key Classes
- `CVGenerator`: Main class that manages Jinja2 environment and handles HTML→PDF conversion

### Template System
- Templates live in `templates/` directory
- Use Jinja2 syntax with standard CV sections (name, email, experience, education, skills, etc.)
- Modern.html provides A4-sized output with responsive styling
- Template variables come directly from YAML data structure

### Data Flow
YAML file → `load_yaml()` → dict → `CVGenerator.render_html()` → HTML string → `CVGenerator.generate_pdf()` → PDF file

## Common Tasks

**Adding a new template:** Create HTML file in `templates/` directory using Jinja2 syntax. Reference example variables in `example.yaml`.

**Extending CV sections:** Modify `example.yaml` to add new data fields, then update templates to use them via `{{ field_name }}` syntax.

**Handling template errors:** WeasyPrint can be strict about HTML/CSS. Test templates with `uv run cvsmith` and check error messages for HTML structure issues.

## Dependencies

- **Jinja2** (3.1.6): HTML templating
- **PyYAML** (6.0.3): YAML parsing
- **WeasyPrint** (68.1): HTML to PDF conversion
- **Click** (8.3.1): CLI framework
- **pytest** (dev): Testing framework
- **black** (dev): Code formatter

Python 3.13+
