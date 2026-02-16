# CVSmith

A Python library to convert YAML CV data to professional PDF documents using Jinja2 templates.

## Features

- Parse YAML-formatted CV data
- Render A4 HTML pages from custom Jinja2 templates
- Generate PDF files using WeasyPrint

## Dependencies

- Jinja2
- PyYAML
- WeasyPrint
- Click

## Installation

```bash
uv sync
```

## Usage

```bash
uv run cvsmith --yaml data.yaml --template modern.html --output cv.pdf
```

## Project Structure

- `src/cvsmith/` - Main package code
- `templates/` - Jinja2 templates for CV rendering
- `pyproject.toml` - Project configuration with uv

## Development

Install dependencies:
```bash
uv sync --all-extras
```
