#!/usr/bin/env python3
"""Marketverse: Multi-Agent Market Research & Report Generator.

Entry point CLI orchestrating hierarchical CrewAI agents to scrape market data,
analyze corporate financial matrices with Pandas, compile ReportLab PDF reports,
and log execution benchmarks.
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import Marketverse components
import crew.config
from crew.crew import MarketverseCrew
from crew.utils.pdf_generator import compile_pdf_report


def parse_arguments() -> argparse.Namespace:
    """Parse command line flags."""
    parser = argparse.ArgumentParser(
        description="Marketverse: Multi-Agent Market Research & PDF Report Generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--query",
        type=str,
        default="Tech Sector Q3 Analysis",
        help="Target market research topic or sector query"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="data/sample_financials.csv",
        help="Path to corporate financial dataset (CSV)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save generated reports and benchmarks"
    )
    parser.add_argument(
        "--pdf-name",
        type=str,
        default="market_report.pdf",
        help="Filename for the compiled PDF report"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
        help="LLM model identifier for supervisor manager"
    )
    return parser.parse_args()


def main() -> int:
    """Execute Marketverse multi-agent research workflow."""
    args = parse_arguments()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Initialize and run Hierarchical CrewAI Workflow
    crew_orchestrator = MarketverseCrew(
        query=args.query,
        csv_path=args.csv,
        manager_model=args.model
    )
    
    run_result = crew_orchestrator.kickoff()
    markdown_report = run_result["markdown_report"]

    # 2. Save Markdown Report
    md_output_path = output_dir / "market_report.md"
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)
    print(f"[Marketverse] Saved raw Markdown report to: {md_output_path}")

    # 3. Post-Processing: Compile Programmatic A4 PDF with ReportLab
    pdf_output_path = output_dir / args.pdf_name
    print(f"[Marketverse] Compiling typeset A4 PDF report with ReportLab...")
    compiled_pdf = compile_pdf_report(
        markdown_content=markdown_report,
        output_path=str(pdf_output_path),
        query=args.query,
        csv_path=args.csv
    )
    print(f"[Marketverse] Successfully compiled PDF: {compiled_pdf}")
    print(f"[Marketverse] Verified PDF File Size: {os.path.getsize(compiled_pdf):,} bytes")

    # 4. Display Execution Summary
    benchmarks = run_result["benchmarks"]
    print("\n" + "=" * 80)
    print("  WORKFLOW EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print(f"  • Query               : {args.query}")
    print(f"  • Total Duration      : {benchmarks['total_duration_seconds']}s")
    print(f"  • Tasks Completed     : {len(benchmarks['routing_history'])}")
    print(f"  • Benchmarks JSON     : {Path('benchmarks.json').resolve()}")
    print(f"  • Output Markdown     : {md_output_path.resolve()}")
    print(f"  • Output PDF Report   : {pdf_output_path.resolve()}")
    print("=" * 80 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
