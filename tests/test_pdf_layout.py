"""Tests verifying ReportLab PDF layout compilation and styling integrity."""

import os
import pytest
from pathlib import Path

from crew.utils.pdf_generator import (
    MarketversePDFGenerator,
    compile_pdf_report,
    NumberedCanvas,
)


def test_pdf_layout_generation(tmp_path: Path, sample_markdown_report: str, mock_csv_file: Path):
    """Verify the report compiler successfully writes a valid PDF file and does not raise styling exceptions."""
    pdf_out = tmp_path / "test_market_report.pdf"

    # Compile PDF
    result_path = compile_pdf_report(
        markdown_content=sample_markdown_report,
        output_path=str(pdf_out),
        query="Tech Sector Q3 Analysis",
        csv_path=str(mock_csv_file)
    )

    # Verify file was written
    assert os.path.exists(result_path)
    file_size = os.path.getsize(result_path)
    assert file_size > 1000, f"PDF file size too small: {file_size} bytes"

    # Verify PDF magic bytes header
    with open(result_path, "rb") as f:
        header = f.read(5)
    assert header == b"%PDF-", f"Invalid PDF header: {header}"


def test_pdf_generator_components(tmp_path: Path, mock_csv_file: Path):
    """Verify header banner, summary table, and peer table can be built without exceptions."""
    pdf_out = tmp_path / "components_test.pdf"
    generator = MarketversePDFGenerator(output_path=str(pdf_out))

    banner = generator.build_header_banner("Automated AI Testing", "November 23, 2026")
    assert banner is not None

    summary_table = generator.build_pandas_summary_table(str(mock_csv_file))
    assert summary_table is not None

    peers_table = generator.build_corporate_peers_table(str(mock_csv_file))
    assert peers_table is not None


def test_empty_content_pdf_resilience(tmp_path: Path):
    """Verify that an empty or minimal markdown input compiles without crashing."""
    pdf_out = tmp_path / "minimal_test.pdf"
    result_path = compile_pdf_report(
        markdown_content="Minimal text only.",
        output_path=str(pdf_out),
        query="Minimal Query"
    )
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 500
