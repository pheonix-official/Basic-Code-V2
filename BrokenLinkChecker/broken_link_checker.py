```python
#!/usr/bin/env python3

import argparse
import asyncio
import aiohttp
import sys
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Set, Dict, Union, List
import logging

class BrokenLinkChecker:
    def __init__(self):
        self.console = Console()
        self.checked_links: Set[str] = set()
        self.results: Dict[str, Dict[str, Union[int, str]]] = {}
        self.session: aiohttp.ClientSession = None
        self.base_url: str = ""
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def initialize_session(self):
        """Initialize aiohttp session with custom headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = aiohttp.ClientSession(headers=headers, timeout=self.timeout)

    async def close_session(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and should be checked"""
        try:
            result = urlparse(url)
            # Check if URL is relative to base_url
            if not result.netloc:
                return True
            # Check if URL is from the same domain
            return result.netloc == urlparse(self.base_url).netloc
        except Exception:
            return False

    async def check_link(self, url: str) -> None:
        """Check a single link for validity"""
        if url in self.checked_links:
            return

        self.checked_links.add(url)
        
        # Handle relative URLs
        if not urlparse(url).netloc:
            url = urljoin(self.base_url, url)

        try:
            async with self.session.get(url) as response:
                status = response.status
                self.results[url] = {
                    "status": status,
                    "message": "OK" if status == 200 else f"HTTP {status}"
                }
        except asyncio.TimeoutError:
            self.results[url] = {"status": 0, "message": "Timeout"}
        except Exception as e:
            self.results[url] = {"status": 0, "message": str(e)}

    async def process_html(self, html_content: str, base_url: str) -> List[str]:
        """Extract links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href and not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                if self.is_valid_url(href):
                    links.append(urljoin(base_url, href))
        
        return links

    async def check_url(self, url: str):
        """Check a website URL for broken links"""
        self.base_url = url
        try:
            async with self.session.get(url) as response:
                html_content = await response.text()
                links = await self.process_html(html_content, url)
                tasks = [self.check_link(link) for link in links]
                await asyncio.gather(*tasks)
        except Exception as e:
            self.console.print(f"[red]Error accessing {url}: {str(e)}[/red]")

    async def check_directory(self, directory: str):
        """Check HTML files in a directory for broken links"""
        directory_path = Path(directory)
        if not directory_path.exists():
            self.console.print(f"[red]Directory {directory} does not exist[/red]")
            return

        html_files = list(directory_path.glob('**/*.html'))
        for html_file in html_files:
            self.base_url = f"file://{html_file.absolute()}"
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    links = await self.process_html(f.read(), self.base_url)
                    tasks = [self.check_link(link) for link in links]
                    await asyncio.gather(*tasks)
            except Exception as e:
                self.console.print(f"[red]Error processing {html_file}: {str(e)}[/red]")

    def display_results(self, output_format: str = 'table'):
        """Display results in the specified format"""
        if output_format == 'json':
            print(json.dumps(self.results, indent=2))
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("URL")
            table.add_column("Status")
            table.add_column("Message")

            for url, result in self.results.items():
                status = result['status']
                color = "green" if status == 200 else "red"
                table.add_row(
                    url,
                    str(status),
                    result['message'],
                    style=color
                )

            self.console.print(table)

async def main():
    parser = argparse.ArgumentParser(description='Broken Link Checker CLI Tool')
    parser.add_argument('target', help='URL or directory to check')
    parser.add_argument('--format', choices=['table', 'json'], default='table',
                      help='Output format (default: table)')
    args = parser.parse_args()

    checker = BrokenLinkChecker()
    await checker.initialize_session()

    try:
        if args.target.startswith(('http://', 'https://')):
            await checker.check_url(args.target)
        else:
            await checker.check_directory(args.target)
    finally:
        await checker.close_session()

    checker.display_results(args.format)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
```
