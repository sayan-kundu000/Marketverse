"""Tests verifying web scraper tools and text cleaning."""

import pytest
from crew.tools.scraper_tool import (
    clean_html_text,
    get_curated_market_intelligence,
    search_and_scrape_market_data,
    scrape_webpage,
)


def test_clean_html_text():
    """Verify script and style removal and text paragraph extraction."""
    raw_html = """
    <html>
        <head><title>Market Report</title><style>body { color: red; }</style></head>
        <body>
            <script>alert('malicious');</script>
            <nav><a href="#">Home</a></nav>
            <h1>Tech Sector Q3 Earnings</h1>
            <p>Cloud infrastructure revenues grew 24% YoY.</p>
            <footer>Copyright 2026</footer>
        </body>
    </html>
    """
    cleaned = clean_html_text(raw_html)
    assert "Tech Sector Q3 Earnings" in cleaned
    assert "Cloud infrastructure revenues grew 24% YoY." in cleaned
    assert "alert" not in cleaned
    assert "body { color: red; }" not in cleaned
    assert "Home" not in cleaned


def test_curated_market_intelligence():
    """Verify high-fidelity fallback intelligence contains expected financial metrics."""
    data = get_curated_market_intelligence("Tech Sector Q3 Analysis")
    assert "Real-Time Financial Market Intelligence" in data
    assert "Hyperscaler Cloud & AI Acceleration" in data
    assert "NVIDIA Corp (NVDA)" in data
    assert "Microsoft Corp (MSFT)" in data


def test_search_and_scrape_market_data_tool():
    """Verify search and scrape tool executes and returns formatted research text."""
    result = search_and_scrape_market_data.run(query="Tech Sector Q3 Analysis")
    assert isinstance(result, str)
    assert len(result) > 200
    assert "Tech Sector Q3 Analysis" in result
