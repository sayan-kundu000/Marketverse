"""Tests verifying Pandas Analysis math, descriptive statistics, and markdown formatting."""

import pytest
import pandas as pd
from pathlib import Path

from crew.tools.financial_tool import (
    calculate_financial_metrics,
    load_and_preprocess_dataframe,
    get_financial_summary_stats,
    clean_numeric_series,
)


def test_pandas_analysis_mock_csv(mock_csv_file: Path):
    """Verify the data parser tool correctly calculates summary statistics on a mock CSV dataset."""
    result = calculate_financial_metrics.run(csv_path=str(mock_csv_file))

    assert isinstance(result, str)
    assert "### Financial Summary Statistics (Pandas Matrix Analysis)" in result
    assert "mock_test_financials.csv" in result
    assert "Companies Analyzed**: 3" in result

    # Check descriptive statistics table presence
    assert "| count" in result
    assert "| mean" in result
    assert "| std" in result
    assert "| min" in result
    assert "| max" in result

    # Verify exact mathematical calculations:
    # Revenue: [100.0, 200.0, 300.0] -> mean = 200.0, min = 100.0, max = 300.0
    # Growth: [10.0, 20.0, 30.0] -> mean = 20.0
    # Margin: [20.0, 30.0, 40.0] -> mean = 30.0
    # PE: [25.0, 35.0, 45.0] -> mean = 35.0
    df = load_and_preprocess_dataframe(str(mock_csv_file))
    summary = get_financial_summary_stats(df)

    assert summary.loc["count", "Revenue_Billions"] == 3.0
    assert summary.loc["mean", "Revenue_Billions"] == 200.0
    assert summary.loc["min", "Revenue_Billions"] == 100.0
    assert summary.loc["max", "Revenue_Billions"] == 300.0
    assert summary.loc["std", "Revenue_Billions"] == 100.0

    assert summary.loc["mean", "YoY_Growth_Pct"] == 20.0
    assert summary.loc["mean", "Operating_Margin_Pct"] == 30.0
    assert summary.loc["mean", "PE_Ratio"] == 35.0

    # Verify key aggregate indicators in markdown text
    assert "$600.00B" in result  # Total aggregate revenue
    assert "$200.00B" in result  # Average company revenue


def test_clean_numeric_series_formats():
    """Verify cleaning of currency symbols, percentages, and commas."""
    raw = pd.Series(["$1,250.50", "$3,400.00", "500", "$100,000.75"])
    cleaned = clean_numeric_series(raw)
    assert cleaned.iloc[0] == 1250.50
    assert cleaned.iloc[1] == 3400.00
    assert cleaned.iloc[2] == 500.0
    assert cleaned.iloc[3] == 100000.75

    pct_raw = pd.Series(["15.5%", "24.0%", "8.2%"])
    cleaned_pct = clean_numeric_series(pct_raw)
    assert cleaned_pct.iloc[0] == 15.5
    assert cleaned_pct.iloc[1] == 24.0


def test_missing_csv_fallback():
    """Verify graceful handling and fallback to default dataset when csv path is invalid."""
    result = calculate_financial_metrics.run(csv_path="non_existent_file.csv")
    assert "### Financial Summary Statistics (Pandas Matrix Analysis)" in result
    assert "sample_financials.csv" in result
