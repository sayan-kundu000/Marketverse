"""Financial Data Parser Tool for Marketverse.

Parses tabular corporate metrics using Pandas, cleans numeric columns,
calculates statistical summaries (mean, min, max, standard deviations),
and returns clean Markdown tables for agent synthesis and report compilation.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd

# Ensure crewai environment config is loaded
import crew.config  # noqa: F401
from crewai.tools import tool

# Default fallback dataset path
DEFAULT_CSV_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "sample_financials.csv"


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """Clean strings containing $, %, commas and convert to numeric float."""
    if pd.api.types.is_numeric_dtype(series):
        return series
    
    cleaned = (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def load_and_preprocess_dataframe(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Load a corporate financial metrics CSV file into a sanitized Pandas DataFrame."""
    target_path = Path(csv_path) if csv_path and os.path.exists(csv_path) else DEFAULT_CSV_PATH
    
    if not target_path.exists():
        raise FileNotFoundError(f"Financial dataset not found at: {target_path}")

    df = pd.read_csv(target_path)

    # Clean numeric columns
    for col in df.columns:
        if col.lower() not in ("company", "ticker", "symbol", "name", "sector", "industry"):
            df[col] = clean_numeric_series(df[col])

    return df


def get_financial_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute comprehensive statistical distribution for numeric financial metrics."""
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty:
        raise ValueError("No numeric financial metrics found in dataset")
    
    # describe() provides count, mean, std, min, 25%, 50%, 75%, max
    summary = numeric_df.describe().round(2)
    return summary


@tool("calculate_financial_metrics")
def calculate_financial_metrics(csv_path: str) -> str:
    """Loads corporate metrics from CSV and returns summary statistics as Markdown."""
    path = csv_path.strip() if csv_path else ""
    if not path or not os.path.exists(path):
        path = str(DEFAULT_CSV_PATH)

    df = load_and_preprocess_dataframe(path)
    summary_df = get_financial_summary_stats(df)
    
    # Format as clean markdown
    summary_markdown = summary_df.to_markdown()

    # Also compute aggregate key indicators
    key_metrics = []
    if "Revenue_Billions" in df.columns:
        key_metrics.append(f"- **Total Aggregate Revenue**: ${df['Revenue_Billions'].sum():.2f}B")
        key_metrics.append(f"- **Average Company Revenue**: ${df['Revenue_Billions'].mean():.2f}B (std: ${df['Revenue_Billions'].std():.2f}B)")
    if "YoY_Growth_Pct" in df.columns:
        key_metrics.append(f"- **Mean YoY Growth Rate**: {df['YoY_Growth_Pct'].mean():.1f}% (Range: {df['YoY_Growth_Pct'].min():.1f}% - {df['YoY_Growth_Pct'].max():.1f}%)")
    if "Operating_Margin_Pct" in df.columns:
        key_metrics.append(f"- **Average Operating Margin**: {df['Operating_Margin_Pct'].mean():.1f}% (Median: {df['Operating_Margin_Pct'].median():.1f}%)")
    if "PE_Ratio" in df.columns:
        key_metrics.append(f"- **Median P/E Multiple**: {df['PE_Ratio'].median():.1f}x (Mean: {df['PE_Ratio'].mean():.1f}x)")
    if "Market_Cap_Billions" in df.columns:
        key_metrics.append(f"- **Total Combined Market Cap**: ${df['Market_Cap_Billions'].sum():.2f}B")

    key_summary = "\n".join(key_metrics)

    output = (
        f"### Financial Summary Statistics (Pandas Matrix Analysis)\n\n"
        f"**Analyzed Dataset**: `{Path(path).name}` | **Companies Analyzed**: {len(df)}\n\n"
        f"#### Descriptive Statistics Table\n"
        f"{summary_markdown}\n\n"
        f"#### Key Aggregate Indicators\n"
        f"{key_summary}\n"
    )
    return output


def get_raw_table_for_report(csv_path: Optional[str] = None) -> Tuple[List[str], List[List[Any]]]:
    """Retrieve tabular data formatted for ReportLab PDF compilation."""
    df = load_and_preprocess_dataframe(csv_path)
    columns = [col.replace("_", " ") for col in df.columns]
    data = df.values.tolist()
    return columns, data


def get_summary_table_for_report(csv_path: Optional[str] = None) -> Tuple[List[str], List[List[Any]]]:
    """Retrieve summary statistics formatted for ReportLab PDF compilation."""
    df = load_and_preprocess_dataframe(csv_path)
    summary_df = get_financial_summary_stats(df).reset_index()
    summary_df.rename(columns={"index": "Statistic"}, inplace=True)
    columns = [col.replace("_", " ") for col in summary_df.columns]
    data = summary_df.values.tolist()
    return columns, data
