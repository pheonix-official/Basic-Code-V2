```markdown
# Broken Link Checker CLI Tool

A command-line tool that recursively scans websites or directories for broken links. This tool can help you identify broken links (404 errors, timeouts, etc.) in your web projects or documentation.

## Features

- Accepts both website URLs and local directory paths as input
- Recursively scans HTML files for links
- Asynchronous link checking for improved performance
- Detects various link issues (404s, timeouts, connection errors)
- Multiple output formats (table and JSON)
- User-friendly colored output
- Handles relative and absolute URLs
- Respects same-domain policy for web crawling

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Check a website:
```bash
python broken_link_checker.py https://example.com
```

### Check local HTML files:
```bash
python broken_link_checker.py ./path/to/html/files
```

### Output in JSON format:
```bash
python broken_link_checker.py https://example.com --format json
```

## Output Formats

### Table Format (Default)
The table format provides a clear, colored overview of all checked links with their status and any error messages.

### JSON Format
JSON output is available for programmatic processing of results.

## Error Handling

The tool handles various error cases:
- Connection timeouts
- 404 Not Found errors
- DNS resolution errors
- Invalid URLs
- File access errors

## Performance

The tool uses `aiohttp` for asynchronous HTTP requests, making it efficient when checking multiple links. It also implements:
- Connection pooling
- Timeout handling
- Concurrent requests
- Memory-efficient processing

## Limitations

- Only checks links within the same domain when scanning websites
- Requires proper permissions for accessing local files
- May be blocked by some websites' robot policies

