"""Task definitions for Marketverse Hierarchical Crew."""

from typing import Optional
from crewai import Task, Agent


def create_research_task(
    agent: Agent,
    query: str = "Tech Sector Q3 Analysis",
    csv_path: Optional[str] = None
) -> Task:
    """Create the market research and web scraping task."""
    return Task(
        description=(
            f"Query search networks and scrape financial data for market topic: '{query}'.\n"
            f"1. Use search_and_scrape_market_data to retrieve live market intelligence, recent earnings, "
            f"and capex trends.\n"
            f"2. Scrape key industry web sources and extract corporate metrics for leading market participants.\n"
            f"3. Highlight secular demand trends, competitive dynamics, and structural market catalysts.\n"
            f"4. Provide a well-organized research dossier with source citations."
        ),
        expected_output=(
            "A comprehensive market research dossier summarizing industry dynamics, revenue drivers, "
            "corporate performance highlights, and extracted market intelligence."
        ),
        agent=agent
    )


def create_analysis_task(
    agent: Agent,
    csv_path: Optional[str] = None
) -> Task:
    """Create the quantitative Pandas financial analysis task."""
    target_csv = csv_path or "data/sample_financials.csv"
    return Task(
        description=(
            f"Perform rigorous computational data parsing on corporate metrics in '{target_csv}'.\n"
            f"1. Use calculate_financial_metrics to compute descriptive statistics (count, mean, std, "
            f"min, 25%, 50%, 75%, max).\n"
            f"2. Verify numeric consistency across revenue figures, growth percentages, margins, and P/E ratios.\n"
            f"3. Generate a clean Markdown summary table and calculate aggregate sector benchmarks.\n"
            f"4. Highlight top performers, outliers, and margin distribution patterns."
        ),
        expected_output=(
            "A complete quantitative analysis featuring the Pandas summary statistics Markdown table, "
            "aggregate financial indicators, and variance consistency notes."
        ),
        agent=agent
    )


def create_writing_task(
    agent: Agent,
    query: str = "Tech Sector Q3 Analysis"
) -> Task:
    """Create the technical report synthesis and writing task."""
    return Task(
        description=(
            f"Synthesize the research dossier and quantitative Pandas financial statistics into an "
            f"authoritative, comprehensive Market Research Report on '{query}'.\n"
            f"Structure the report with the following mandatory sections:\n"
            f"# Market Research Report: {query}\n"
            f"## 1. Executive Summary & Market Snapshot\n"
            f"## 2. Sector Growth Drivers & Strategic Technology Catalysts\n"
            f"## 3. Quantitative Financial Matrix & Descriptive Statistics\n"
            f"   (Embed the verified Pandas Markdown summary table and aggregate indicators)\n"
            f"## 4. Peer Group Valuation & Competitive Benchmarking\n"
            f"## 5. Risk Factors, Sensitivity Analysis & Strategic Outlook\n\n"
            f"Ensure professional styling, precise tone, and publication-ready formatting."
        ),
        expected_output=(
            "A publication-ready, fully structured market research report in Markdown format, "
            "incorporating all required sections, Pandas tabular statistics, and executive synthesis."
        ),
        agent=agent
    )
