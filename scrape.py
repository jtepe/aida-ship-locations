#!/usr/bin/env python3
"""Scrape AIDA ship positions using Playwright to bypass bot protection."""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def scrape_ship_positions(url: str, output_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            },
        )
        page = context.new_page()

        print(f"Fetching {url}")
        response = page.goto(url, wait_until="networkidle", timeout=30000)

        if response is None or not response.ok:
            status = response.status if response else "no response"
            print(f"Error: Failed to fetch URL (status: {status})")
            browser.close()
            sys.exit(1)

        content = page.content()

        if "Access Denied" in content:
            print("Error: Access denied by server")
            browser.close()
            sys.exit(1)

        output_path.write_text(content, encoding="utf-8")
        print(f"Saved to {output_path}")

        browser.close()


def main() -> None:
    url = "https://www.aida.de/webcam/shippositions.xml"
    output_path = Path("aida.de-webcam-shippositions.xml")
    scrape_ship_positions(url, output_path)


if __name__ == "__main__":
    main()
