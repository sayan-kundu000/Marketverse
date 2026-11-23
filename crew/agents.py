"""Specialized Agent definitions for Marketverse Hierarchical Team.

Implements three specialized CrewAI agents managed hierarchically:
1. Lead Researcher Agent ('Market Research Specialist')
2. Data Analyst Agent ('Financial Data Analyst')
3. Content Writer Agent ('Technical Reports Writer')
"""

import os
from typing import Optional, Any
import crew.config  # Initializes sandboxed environment and loads .env
from crewai import Agent
from crewai.llm import LLM
from crew.tools.scraper_tool import search_and_scrape_market_data, scrape_webpage
from crew.tools.financial_tool import calculate_financial_metrics


def get_llm(model_name: Optional[str] = None) -> Any:
    """Resolve configured LLM instance or return standard LLM."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    target_model = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    # If an API key is missing or dummy placeholder, provide a fallback key for model schema validation
    if not api_key or api_key == "your_openai_api_key_here":
        api_key = "mock_marketverse_key"

    try:
        return LLM(model=target_model, api_key=api_key)
    except Exception:
        return LLM(model="gpt-4o", api_key=api_key)


def create_lead_researcher_agent(llm: Optional[Any] = None) -> Agent:
    """Creates the Lead Researcher Agent.
    
    Role: 'Market Research Specialist'
    Goal: Query search search networks, locate financial data, and scrape company metrics.
    """
    return Agent(
        role="Market Research Specialist",
        goal="Query search search networks, locate financial data, and scrape company metrics.",
        backstory=(
            "You are a seasoned Market Research Specialist with deep expertise in financial "
            "search discovery, scraping SEC filings, quarterly earnings transcripts, "
            "and market sentiment intelligence. You extract high-signal qualitative "
            "and quantitative metrics and provide thorough, well-sourced evidence."
        ),
        tools=[search_and_scrape_market_data, scrape_webpage],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_data_analyst_agent(llm: Optional[Any] = None) -> Agent:
    """Creates the Data Analyst Agent.
    
    Role: 'Financial Data Analyst'
    Goal: Parse data matrices using Pandas, compute averages, and verify numeric consistency.
    """
    return Agent(
        role="Financial Data Analyst",
        goal="Parse data matrices using Pandas, compute averages, and verify numeric consistency.",
        backstory=(
            "You are an expert Financial Data Analyst skilled in computational statistics and "
            "Pandas data manipulation. You scrutinize corporate metrics, compute summary distributions "
            "(means, medians, standard deviations, min/max), cross-verify numeric consistency, and "
            "generate clean Markdown tables that ground technical reports in mathematical rigor."
        ),
        tools=[calculate_financial_metrics],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_content_writer_agent(llm: Optional[Any] = None) -> Agent:
    """Creates the Content Writer Agent.
    
    Role: 'Technical Reports Writer'
    Goal: Synthesize information, write sections, and structure copy.
    """
    return Agent(
        role="Technical Reports Writer",
        goal="Synthesize information, write sections, and structure copy.",
        backstory=(
            "You are an elite Technical Reports Writer with years of experience authoring institutional "
            "investment memos and industry whitepapers. You synthesize raw market research and Pandas "
            "statistical summaries into a cohesive, beautifully structured executive report with clear "
            "headings, actionable strategic insights, risk disclosures, and publication-ready prose."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
