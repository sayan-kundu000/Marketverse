"""Tests verifying command-line interface arguments and execution."""

import os
import subprocess
import sys
import pytest
from pathlib import Path

from main import parse_arguments


def test_cli_argument_parsing(monkeypatch):
    """Verify CLI defaults and custom flag overrides."""
    test_args = [
        "main.py",
        "--query", "Semiconductor Q4 Analysis",
        "--csv", "data/sample_financials.csv",
        "--output-dir", "custom_output",
        "--pdf-name", "custom_report.pdf",
        "--model", "gpt-4o-mini"
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    args = parse_arguments()

    assert args.query == "Semiconductor Q4 Analysis"
    assert args.csv == "data/sample_financials.csv"
    assert args.output_dir == "custom_output"
    assert args.pdf_name == "custom_report.pdf"
    assert args.model == "gpt-4o-mini"


def test_cli_defaults(monkeypatch):
    """Verify default arguments match project requirements."""
    monkeypatch.setattr(sys, "argv", ["main.py"])
    args = parse_arguments()

    assert args.query == "Tech Sector Q3 Analysis"
    assert args.csv == "data/sample_financials.csv"
    assert args.output_dir == "output"
    assert args.pdf_name == "market_report.pdf"
