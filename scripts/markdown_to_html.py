#!/usr/bin/env python3
"""
Convert Markdown files to HTML with syntax highlighting.
Default CSS file is style.css 

Dependencies:
    pip install markdown pygments

Usage:
    # Basic conversion
    python scripts/markdown_to_html.py --input README.md

    # Specify output HTML file and page title
    python scripts/markdown_to_html.py -i README.md -o README.html -t "My Page"

    # Optional custom CSS
    python scripts/markdown_to_html.py -i README.md -o README.html -t "My Page" --css style.css
"""

import argparse
from pathlib import Path
import markdown
from pygments.formatters import HtmlFormatter

def convert_md_to_html(
    md_file: Path,
    output_file: Path,
    page_title: str = "",
    css_file: Path = None,
):
    if not md_file.exists():
        print(f"Error: {md_file} does not exist.")
        return

    text = md_file.read_text(encoding="utf-8")

    # Syntax highlighting using pygments
    extensions = ["fenced_code", "codehilite", "tables"]
    md = markdown.Markdown(extensions=extensions)

    html_content = md.convert(text)

    # Add CSS
    style = ""
    if css_file and css_file.exists():
        style += css_file.read_text(encoding="utf-8") + "\n"

    # Add pygments CSS (built-in style 'monokai')
    formatter = HtmlFormatter(style="monokai")
    style += formatter.get_style_defs(".codehilite")

    # HTML pre/post content
    pre_content = f"""<html>
<head>
    <title>{page_title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
</head>
<body>
    <div id='content'>
"""

    post_content = f"""
    </div>
    <style type='text/css'>
{style}
    </style>
</body>
</html>
"""

    html = pre_content + html_content + post_content

    if output_file.exists():
        print(f"File '{output_file}' already exists. Aborted!")
        return

    output_file.write_text(html, encoding="utf-8")
    print(f"Done, saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML with syntax highlighting")
    parser.add_argument('--input', '-i', type=Path, default="README.md", help="Markdown file to convert")
    parser.add_argument('--output', '-o', type=Path, help="Output HTML file path")
    parser.add_argument('--title', '-t', type=str, default="", help="Page title")
    parser.add_argument('--css', '-c', type=Path, help="Optional CSS file")
    args = parser.parse_args()

    output_file = args.output or args.input.with_suffix(".html")

    convert_md_to_html(args.input, output_file, args.title, args.css)

if __name__ == "__main__":
    main()
