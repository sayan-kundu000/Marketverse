"""Pytest configuration and shared fixtures for Marketverse test suite."""

import os
import sys
import tempfile
import pytest
from pathlib import Path

# Ensure workspace root and crew package are importable
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure sandboxed environment variables
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("MARKETVERSE_OFFLINE_MODE", "true")

workspace_localappdata = BASE_DIR / ".localappdata"
workspace_localappdata.mkdir(parents=True, exist_ok=True)
os.environ["LOCALAPPDATA"] = str(workspace_localappdata)


@pytest.fixture
def mock_csv_file(tmp_path: Path) -> Path:
    """Create a controlled mock CSV dataset with known mathematical properties."""
    csv_content = (
        "Company,Ticker,Revenue_Billions,YoY_Growth_Pct,Operating_Margin_Pct,PE_Ratio\n"
        "Alpha Corp,ALPH,100.0,10.0,20.0,25.0\n"
        "Beta Corp,BETA,200.0,20.0,30.0,35.0\n"
        "Gamma Corp,GAMM,300.0,30.0,40.0,45.0\n"
    )
    file_path = tmp_path / "mock_test_financials.csv"
    file_path.write_text(csv_content, encoding="utf-8")
    return file_path


@pytest.fixture
def sample_markdown_report() -> str:
    """Provide a structured markdown sample for PDF layout testing."""
    return """# Market Research Report: Tech Sector Q3 Analysis
## 1. Executive Summary
Enterprise IT fundamentals remain exceptionally resilient across cloud and AI verticals.
- Cloud infrastructure growth reached 24% YoY.
- AI capex intensity continues to expand at historic rates.

## 2. Sector Growth Drivers & Catalysts
Semiconductor advanced packaging and high-bandwidth memory remain key technological bottlenecks.

## 3. Quantitative Financial Matrix & Descriptive Statistics
The following metrics reflect cohort performance.

## 4. Peer Group Valuation & Benchmarking
Multiples reflect healthy free cash flow conversion.

## 5. Risk Factors & Strategic Outlook
Grid interconnect delays pose medium-term challenges.
"""
