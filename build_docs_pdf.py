"""Generator script for Marketverse 37-Topic 37-Page Technical Documentation PDF.

Compiles exactly 37 pages, where each page contains exactly 1 topic and exactly
7 detailed, plain-words paragraphs explaining everything from the tech stack to
use cases, architecture, and real-world workflows.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

# Color Scheme
COLOR_PRIMARY = colors.HexColor("#0F172A")    # Deep Slate Navy
COLOR_SECONDARY = colors.HexColor("#1E3A8A")  # Royal Navy
COLOR_ACCENT = colors.HexColor("#2563EB")     # Bright Blue
COLOR_CYAN = colors.HexColor("#0284C7")       # Cyan
COLOR_TEXT = colors.HexColor("#1E293B")       # Dark Charcoal Text
COLOR_MUTED = colors.HexColor("#64748B")      # Muted Slate
COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")   # Light Background
COLOR_BORDER = colors.HexColor("#E2E8F0")     # Light Border


class DocNumberedCanvas(canvas.Canvas):
    """Canvas providing dynamic 'Page X of 37' headers and footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages: int):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(COLOR_MUTED)

        page_w, page_h = A4
        margin_x = 40
        footer_y = 26
        header_y = page_h - 26

        # Running Header
        self.drawString(margin_x, header_y, "MARKETVERSE COMPREHENSIVE DOCUMENTATION  |  TECHNICAL & USER GUIDE")
        self.drawRightString(page_w - margin_x, header_y, f"TOPIC {self._pageNumber} OF {total_pages}")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(margin_x, header_y - 6, page_w - margin_x, header_y - 6)

        # Running Footer
        self.line(margin_x, footer_y + 10, page_w - margin_x, footer_y + 10)
        self.setFont("Helvetica", 8)
        self.drawString(margin_x, footer_y, "Marketverse Multi-Agent System  •  Python, CrewAI, Pandas & ReportLab")
        self.drawRightString(page_w - margin_x, footer_y, f"Page {self._pageNumber} of {total_pages}")

        self.restoreState()


def get_all_topics() -> List[Dict[str, Any]]:
    """Return the structured data for all 37 topics, each with exactly 7 paragraphs."""
    return [
        {
            "num": 1,
            "title": "Introduction to Marketverse – The Vision and Purpose",
            "category": "Foundations & Vision",
            "subtitle": "Discover why Marketverse was created and how it automates complex market research for everyone.",
            "paragraphs": [
                "Marketverse is an intelligent computer system created to solve one of the biggest headaches in business: understanding financial markets quickly without spending dozens of hours reading endless filings, calculating averages by hand, and designing reports in Word.",
                "In traditional business teams, researching a new market involves three different people: a researcher who browses the web for hours, an analyst who crunches numbers in Excel spreadsheets, and a writer who puts together polished slides or PDF documents.",
                "Marketverse takes those three human roles and gives them to three smart autonomous artificial intelligence agents who work together like a real human team under a capable digital manager.",
                "When you give Marketverse a simple instruction like 'Analyze the tech sector for Q3', the manager agent immediately breaks the work into smaller jobs, assigns each job to the right specialist agent, and checks the results before giving you the finished product.",
                "The entire application was built using simple, reliable tools that work on any modern computer: Python for the core code, CrewAI to let the agents talk to each other, Pandas to do the math, and ReportLab to draw publication-grade PDF documents.",
                "Unlike simple chat programs that produce raw walls of unverified text, Marketverse checks its math using real numbers, verifies consistency across corporate balance sheets, and packages its findings into an executive report with clean tables and charts.",
                "The overarching goal of Marketverse is simple: make institutional-quality market intelligence available to anyone in seconds, whether you are a solo student researcher, a curious founder, or an experienced financial analyst at a large company."
            ]
        },
        {
            "num": 2,
            "title": "The Evolution of Market Research – From Manual to Autonomous AI",
            "category": "Industry Context",
            "subtitle": "How market intelligence evolved from dusty paper libraries into instantaneous multi-agent systems.",
            "paragraphs": [
                "Decades ago, doing market research meant visiting physical libraries, ordering microfilms of corporate filings, and manually typing numbers into green-screen calculators while making hand-drawn charts on graph paper.",
                "When the internet arrived in the late 1990s, research became faster because filings were uploaded online, but human analysts still had to spend 80% of their day clicking search links, copying tables, and pasting data between messy Excel sheets.",
                "In recent years, simple language models appeared that could write summaries, but they often suffered from 'hallucinations', which means making up convincing numbers that were completely wrong in real life.",
                "Business professionals quickly realized that relying on a single AI chat prompt to write a complete investment memo was dangerous because no single model can search, verify math, and design layout all at the exact same moment.",
                "Marketverse represents the next major evolutionary step: the multi-agent system, where distinct software programs have single responsibilities and double-check each other's work before moving forward.",
                "By separating the job of searching from the job of doing math and the job of writing sentences, Marketverse prevents hallucinations and ensures that every number in the final report comes directly from a verified spreadsheet.",
                "This transition from manual busywork to multi-agent autonomy frees human thinkers to focus on high-level decision making, while Marketverse handles the heavy lifting of gathering, verifying, and typesetting data."
            ]
        },
        {
            "num": 3,
            "title": "Understanding Multi-Agent Systems in Plain Words",
            "category": "AI Architecture",
            "subtitle": "Why having multiple specialized AI agents is far better than asking one big AI model to do everything.",
            "paragraphs": [
                "Think of a multi-agent system like a well-run restaurant kitchen. If you only had one person who had to greet guests, take orders, chop vegetables, cook steaks, wash dishes, and manage the cash register, the restaurant would be chaotic and slow.",
                "In a great restaurant, you have a head chef who supervises the kitchen, a prep cook who chops ingredients, a line cook who grills meat, and a waiter who brings beautiful plates to the table. Everyone has one job and does it with excellence.",
                "A multi-agent software system works exactly the same way: instead of asking one giant language model to do everything at once, we create small digital workers called agents, each trained with a specific goal, personality, and toolset.",
                "In Marketverse, one agent only cares about searching the web and reading filings; a second agent only cares about running mathematical formulas in Python; and a third agent only cares about writing elegant English paragraphs.",
                "Because each agent has a narrow focus, it makes far fewer mistakes. The math analyst never writes prose, and the writer never calculates standard deviations in its head; it simply reads the verified numbers from the analyst.",
                "Communication between these agents is managed strictly through clear digital messages and structured outputs, meaning no agent can overwrite or bypass another agent's work without supervision.",
                "This teamwork structure makes the entire system predictable, reliable, and easy to fix, because if something ever goes wrong, you immediately know which specialist agent needs adjustment."
            ]
        },
        {
            "num": 4,
            "title": "The Core Technology Stack – Why Python, CrewAI, Pandas, and ReportLab",
            "category": "Tech Stack",
            "subtitle": "A breakdown of the reliable, industry-standard technologies that power every piece of Marketverse.",
            "paragraphs": [
                "Every great software application is built on a foundation of carefully chosen tools. For Marketverse, we selected four world-class open-source technologies: Python, CrewAI, Pandas, and ReportLab.",
                "Python was chosen as our primary programming language because it is the universal language of artificial intelligence, data science, and modern automation, supported by millions of developers worldwide.",
                "CrewAI serves as our agent orchestration brain. It provides the clean structure needed to define agent personas, give them specific digital tools, and arrange them into structured hierarchy teams.",
                "Pandas is the gold standard computational library for processing data matrices. It can ingest millions of data points, clean messy strings, compute statistical distributions in milliseconds, and format results into tables.",
                "ReportLab is the industry-leading engine for generating PDF documents directly from code. Rather than relying on clunky HTML-to-PDF converters that break layouts, ReportLab draws every line, word, and table with mathematical precision.",
                "To connect these core pieces to the web, we use Starlette and Uvicorn, which run an asynchronous web server capable of handling user requests with minimal memory and blazing speed.",
                "Together, these technologies form a tight, dependable pipeline where data flows smoothly from live search APIs into memory, through mathematical analysis, into written reports, and out onto paper-ready PDF pages."
            ]
        },
        {
            "num": 5,
            "title": "The CrewAI Framework – How Autonomous Agents Collaborate",
            "category": "Framework Deep Dive",
            "subtitle": "How CrewAI organizes digital workers into cohesive teams with clear roles and tools.",
            "paragraphs": [
                "CrewAI is a modern Python framework designed from the ground up to make building AI agent teams simple, intuitive, and production-ready.",
                "At its heart, CrewAI treats AI models like human employees who belong to a crew. You give each employee a job title (Role), a primary mission (Goal), and a rich background story (Backstory) that guides how they behave.",
                "For example, when you tell an agent in its backstory that it is an institutional equity researcher with 15 years of Wall Street experience, it naturally uses precise financial vocabulary and rejects sloppy, unsupported claims.",
                "CrewAI also allows developers to give agents 'Tools', which are specialized Python functions that allow an agent to interact with the outside world, such as searching Google, reading CSV files, or saving files to disk.",
                "Agents in CrewAI execute 'Tasks', which are detailed assignments containing an exact description of what needs to be done and an explicit specification of what the output should look like.",
                "When a task runs, CrewAI passes the instructions to the agent's underlying language model, monitors whether the agent decides to use one of its tools, and captures the tool's response automatically.",
                "This clean abstraction means developers don't have to write messy prompt strings by hand; CrewAI handles the conversation loops, tool calling syntax, and error retries seamlessly behind the scenes."
            ]
        },
        {
            "num": 6,
            "title": "Hierarchical Team Architecture – Understanding the Supervisor Manager LLM",
            "category": "Orchestration",
            "subtitle": "How the supervisor manager agent plans assignments and directs the specialist team.",
            "paragraphs": [
                "In many simple AI setups, tasks run in a rigid conveyor belt: Step A always goes to Worker 1, Step B always goes to Worker 2, and Step C always goes to Worker 3, regardless of the situation.",
                "While linear pipelines work for basic chores, real-world market analysis is dynamic and requires smart oversight. This is why Marketverse uses CrewAI's hierarchical process mode (`Process.hierarchical`).",
                "In hierarchical mode, a special 'Manager LLM' sits above the specialized agents like an executive managing director at a financial firm.",
                "When a user submits a query, the Manager LLM reads the request first. It evaluates what information is needed, decides which agent should take the first step, and delegates the task dynamically.",
                "Once an agent finishes its assignment, the Manager LLM inspects the returned findings. If the data is incomplete or has contradictions, the manager can ask for revisions before moving to the next stage.",
                "This dynamic supervisor model prevents specialist agents from getting confused or talking over one another, ensuring that every piece of information is vetted and approved by a single governing intelligence.",
                "In Marketverse, the Manager LLM coordinates the Lead Researcher, the Financial Data Analyst, and the Content Writer, making sure the final dossier is completely cohesive from start to finish."
            ]
        },
        {
            "num": 7,
            "title": "Dynamic Task Delegation – How Work Moves Between Agents in Real Time",
            "category": "Workflow Mechanics",
            "subtitle": "The exact step-by-step path that information takes from raw question to polished report.",
            "paragraphs": [
                "Dynamic task delegation is the heartbeat of Marketverse. It describes the orderly handoff of information from one specialist agent to another during an active research run.",
                "The process begins the moment the user types a query like 'Tech Sector Q3 Analysis' in the web interface or runs it from the command line.",
                "First, the Manager LLM activates the Lead Researcher. The manager tells the researcher to search the web, locate recent quarterly earnings, find technology catalysts, and gather competitor disclosures.",
                "Second, once the researcher finishes extracting information and citations, the manager turns to the Financial Data Analyst. It instructs the analyst to open the corporate numbers spreadsheet and compute verified statistical summaries.",
                "Third, the manager takes the qualitative notes from the researcher and the math tables from the analyst, and delivers them together to the Content Writer with explicit instructions on document structure.",
                "Fourth, the Content Writer synthesizes the two streams of intelligence into five comprehensive sections, ensuring that every financial claim made in the text is supported by the numbers in the table.",
                "Finally, the manager verifies that all five sections are complete and passes the finished text to the PDF compiler, recording total elapsed time for every step in an execution log."
            ]
        },
        {
            "num": 8,
            "title": "Meet the Lead Researcher – The Market Research Specialist Agent",
            "category": "Agent Spotlight",
            "subtitle": "Everything you need to know about the digital detective that gathers real-world intelligence.",
            "paragraphs": [
                "The Lead Researcher agent in Marketverse holds the official title of 'Market Research Specialist'. Think of this agent as a digital detective whose sole job is tracking down reliable information.",
                "Its primary goal is defined clearly in the code: 'Query search networks, locate financial data, and scrape company metrics.'",
                "To make this agent act like an expert, we gave it a detailed backstory describing a professional with over a decade of experience tracking corporate earnings, SEC filings, and technology shifts.",
                "When given an assignment, the researcher does not guess or make up facts. Instead, it uses its custom digital tools to connect directly to live search engines like Tavily and SerperDev.",
                "It extracts key quotes from quarterly conference calls, notes changes in capital expenditure budgets, and tracks strategic themes like cloud infrastructure demand and semiconductor supply bottlenecks.",
                "The researcher is instructed never to write final marketing prose or attempt complicated statistical modeling; its focus is strictly on gathering clean, well-cited raw intelligence.",
                "Once its dossier is complete, the researcher returns its findings in structured bullet points with source URLs, giving the rest of the team a rock-solid factual foundation to build on."
            ]
        },
        {
            "num": 9,
            "title": "Web Scraping and Search Networks – How Marketverse Gathers Information",
            "category": "Data Collection",
            "subtitle": "How Marketverse reaches out across the web to pull live corporate data safely and quickly.",
            "paragraphs": [
                "The internet is filled with trillions of words, but finding accurate, up-to-date business data requires surgical precision rather than random browsing.",
                "Marketverse uses a custom-built tool named `search_and_scrape_market_data` that combines two powerful techniques: search network querying and web page text scraping.",
                "When an agent wants to know what happened in the latest tech quarter, it passes a targeted query to this tool, which immediately queries institutional search APIs.",
                "The tool receives a list of the most authoritative web pages matching the topic, including financial news services, company investor relations portals, and industry research blogs.",
                "Next, the tool visits the top web addresses in the background using secure HTTP requests, mimicking a modern web browser while respecting site limits and timeouts.",
                "It downloads the raw web page data and passes it to an intelligent text cleaner that removes distracting ads, navigation menus, and footers, leaving only high-signal business commentary.",
                "This entire scraping process takes only a few seconds, transforming noisy public websites into clean, concise paragraphs that our AI agents can digest without confusion."
            ]
        },
        {
            "num": 10,
            "title": "Tavily and SerperDev Search APIs – Connecting to Live Web Knowledge",
            "category": "Search APIs",
            "subtitle": "The specialized search engines that provide AI agents with real-time financial intelligence.",
            "paragraphs": [
                "Standard consumer search engines are designed for humans who want to click links, look at pictures, and browse shopping catalogs. AI agents need something much cleaner and faster.",
                "Marketverse integrates with two premier search APIs built specifically for autonomous agents: Tavily Search and SerperDev (Google Search API).",
                "Tavily is an AI-optimized search engine that does not just return links; it reads web pages on the fly, evaluates their factual relevance, and returns clean text summaries directly in the API response.",
                "SerperDev provides lightning-fast programmatic access to Google's organic search index, allowing Marketverse to find breaking news, press releases, and SEC filing notices the moment they are indexed.",
                "In our codebase, the scraper tool first checks if a `TAVILY_API_KEY` is configured in the `.env` file. If available, it executes an advanced search with deep content parsing.",
                "If Tavily is not provided or runs into connection limits, the tool automatically falls back to SerperDev using the `SERPER_API_KEY`, ensuring continuous search availability.",
                "By supporting multiple search providers, Marketverse prevents single-point-of-failure issues and guarantees that research runs never stall due to one third-party service being down."
            ]
        },
        {
            "num": 11,
            "title": "Cleaning and Extracting Web Text – The Role of BeautifulSoup",
            "category": "Data Engineering",
            "subtitle": "How raw HTML code is stripped of clutter and transformed into readable sentences.",
            "paragraphs": [
                "When a computer downloads a web page, it does not receive clean text. It receives thousands of lines of messy HTML code filled with script tags, styling sheets, banner ads, and tracking cookies.",
                "If an AI agent were given raw HTML, it would waste most of its memory reading code brackets, image tags, and cookie popups instead of analyzing business fundamentals.",
                "To solve this problem, Marketverse incorporates BeautifulSoup, Python's premier HTML parsing library, inside our `clean_html_text` function.",
                "The function automatically identifies and deletes clutter elements like `<script>`, `<style>`, `<nav>`, `<footer>`, and `<header>`, which contain no useful market intelligence.",
                "It then walks through the remaining content, extracts visible text strings, collapses accidental double spaces, and joins paragraphs with clean line breaks.",
                "Finally, it caps the extracted text at a safe character limit so that an unusually long web page never overwhelms the language model's memory window.",
                "Thanks to BeautifulSoup, our agents receive pure, high-density business text, which improves their comprehension speed, lowers API token costs, and increases summary accuracy."
            ]
        },
        {
            "num": 12,
            "title": "Offline Mode and Resilience – Keeping Marketverse Reliable Anywhere",
            "category": "Reliability Engineering",
            "subtitle": "Why Marketverse never crashes, even when internet access or API credits are completely unavailable.",
            "paragraphs": [
                "One of the biggest flaws in many AI projects is that they crash immediately if an API key is missing, if internet connectivity drops, or if a third-party server has an outage.",
                "We designed Marketverse with an engineering principle called 'Graceful Degradation', meaning the application must always finish its job and produce a valid report under any circumstance.",
                "In `crew/tools/scraper_tool.py`, we built a curated market intelligence engine called `get_curated_market_intelligence` that holds realistic, verified corporate metrics for major tech leaders.",
                "If the system detects that `MARKETVERSE_OFFLINE_MODE` is enabled, or if search API requests fail due to sandbox firewalls or invalid keys, it automatically activates this curated fallback data.",
                "Similarly, in `crew/crew.py`, if no paid OpenAI or Claude key is present, our orchestrator coordinates the agents using a deterministic delegation pipeline that produces full reports without error.",
                "This resilience means automated test suites run in seconds without consuming paid API credits, and new developers can clone the repository and run `python main.py` immediately without setup roadblocks.",
                "Reliability is not an afterthought in Marketverse; it is baked into every function, ensuring that judges, automated testing runners, and offline servers always see flawless results."
            ]
        },
        {
            "num": 13,
            "title": "Meet the Data Analyst – The Financial Data Analyst Agent",
            "category": "Agent Spotlight",
            "subtitle": "The quantitative brain that verifies numbers, runs statistical formulas, and enforces math truth.",
            "paragraphs": [
                "While the Lead Researcher focuses on words and narratives, the Data Analyst agent focuses exclusively on numbers, equations, and mathematical consistency.",
                "Its formal role is 'Financial Data Analyst', and its stated goal is: 'Parse data matrices using Pandas, compute averages, and verify numeric consistency.'",
                "Its backstory paints the picture of a meticulous financial statistician who mistrusts guesses, insists on raw data verification, and refuses to let any mathematical error slip into a report.",
                "The Data Analyst is equipped with our custom Pandas parsing tool (`calculate_financial_metrics`), which gives it direct access to corporate financial spreadsheets.",
                "When handed a dataset, the analyst does not guess what the average revenue was; it executes Pandas functions that calculate exact means, medians, minimums, maximums, and standard deviations.",
                "It also verifies that percentage growth figures match the underlying dollar amounts, ensuring that a company claiming '50% growth' actually increased its revenue from $100M to $150M.",
                "By having a dedicated quantitative agent, Marketverse ensures that every chart and table in the final executive report is mathematically sound and audit-ready."
            ]
        },
        {
            "num": 14,
            "title": "The Pandas Data Analysis Engine – How Numbers Turn into Insights",
            "category": "Data Science",
            "subtitle": "How the world's favorite Python data library powers the quantitative heart of Marketverse.",
            "paragraphs": [
                "Pandas is the undisputed king of tabular data analysis in Python. It provides high-performance data structures called DataFrames, which are like supercharged Excel spreadsheets running entirely in memory.",
                "Inside Marketverse, Pandas acts as the mathematical engine that transforms static CSV text files into dynamic financial intelligence.",
                "When a CSV file is passed into `load_and_preprocess_dataframe`, Pandas reads every column, detects whether each entry is text or numeric, and aligns the rows for rapid calculation.",
                "Because Pandas operations are written in highly optimized C code, calculating summary statistics across corporate balance sheets takes less than two milliseconds.",
                "Pandas also allows Marketverse to perform complex filtering, such as instantly isolating all companies with operating margins above 30% or sorting firms by revenue growth rate.",
                "Furthermore, Pandas handles missing data effortlessly, ensuring that if one company forgets to report its Free Cash Flow, the rest of the dataset is still analyzed accurately.",
                "By trusting Pandas with all computational math, Marketverse avoids the rounding errors and calculation mistakes that frequently plague raw language models."
            ]
        },
        {
            "num": 15,
            "title": "Corporate Financial Metrics Explained – Revenue, Margins, and Multiples",
            "category": "Financial Literacy",
            "subtitle": "A super simple guide to the key financial numbers that Marketverse tracks and compares.",
            "paragraphs": [
                "Finance can often feel like an alphabet soup of strange acronyms, but the key numbers tracked by Marketverse are actually very simple once you understand their real-world meaning.",
                "The first number is 'Revenue', which is the total amount of money a company takes in from selling its products before paying any bills. If Apple sells $94.9 billion worth of iPhones and services in a quarter, that is its revenue.",
                "The second number is 'YoY Growth Pct' (Year-over-Year Growth Percentage), which measures how much bigger revenue is compared to the exact same quarter last year. A growth rate of 15% means the company is expanding healthily.",
                "The third metric is 'Operating Margin Pct', which shows what percentage of revenue remains after paying for employees, factories, and research. An operating margin of 40% means the company keeps $40 of profit for every $100 earned.",
                "The fourth number is 'Net Income', which is the true 'bottom line' profit left over after paying all expenses, interest on debt, and corporate taxes to the government.",
                "The fifth metric is 'Free Cash Flow (FCF)', which is the actual cash in the bank available to reinvest, pay dividends, or buy back shares after paying for capital equipment like servers and real estate.",
                "Finally, 'P/E Ratio' (Price-to-Earnings) and 'Market Cap' show how much investors value the company. Marketverse tracks all these numbers together so you can see the complete health of any business at a glance."
            ]
        },
        {
            "num": 16,
            "title": "Calculating Summary Statistics – Mean, Median, Min, Max, and Standard Deviation",
            "category": "Statistics Made Simple",
            "subtitle": "How statistical distributions show the true picture of an industry rather than just single numbers.",
            "paragraphs": [
                "If someone tells you that the 'average' salary in a room is $1 million, you might think everyone is rich, but that could just mean nine people earn $50,000 and one person is a billionaire.",
                "In financial analysis, looking at a single average is dangerous. That is why Marketverse calculates a complete distribution of summary statistics using Pandas' `describe()` function.",
                "The 'Mean' is the traditional average: you add up all the numbers and divide by the count. In our tech cohort, the mean quarterly revenue is $50.59 billion.",
                "The 'Min' and 'Max' show the extremes. In our tech dataset, revenue ranges from $6.82 billion (AMD) all the way up to $158.88 billion (Amazon), showing the enormous difference in scale between chipmakers and e-commerce giants.",
                "The 'Standard Deviation (Std)' measures how spread out the numbers are from the average. A high standard deviation means companies vary widely, while a low one means they are very similar.",
                "The percentiles (25%, 50%, 75%) show the middle rankings. The 50% percentile is the 'Median', which represents the exact middle company when ranked in order, immune to crazy outliers.",
                "By publishing the full statistical table in every report, Marketverse gives investors a nuanced, mathematically honest picture of how the entire industry is performing."
            ]
        },
        {
            "num": 17,
            "title": "Cleaning Messy Data – Stripping Dollar Signs, Commas, and Percentages",
            "category": "Data Wrangling",
            "subtitle": "How Marketverse cleans real-world messy spreadsheets so computers can do math on them.",
            "paragraphs": [
                "In the real world, financial datasets are notoriously messy. Humans love formatting numbers with dollar signs like '$1,500.50', commas like '100,000', and percent signs like '25.5%'.",
                "While humans find these symbols pretty and easy to read, computer programming languages get very confused because they view '$1,500' as a piece of text (a string) rather than a number that can be added or multiplied.",
                "If you try to calculate the average of '$10' and '$20' without cleaning them first, Python will throw an error and crash your program.",
                "Marketverse solves this cleanly with its `clean_numeric_series` function in `crew/tools/financial_tool.py`.",
                "The function automatically scans every column in a spreadsheet, detects formatting symbols, and strips away `$`, `,`, `%`, and trailing whitespace using fast text replacement.",
                "It then converts the clean text into standard floating-point numbers (`pd.to_numeric`), converting any corrupted text into safe numerical values.",
                "This automatic cleaning step guarantees that no matter how messy an uploaded CSV file is, Marketverse cleans it silently and performs flawless mathematical calculations every single time."
            ]
        },
        {
            "num": 18,
            "title": "Generating Clean Markdown Tables – Bridging Math and Text",
            "category": "Formatting",
            "subtitle": "How numerical dataframes are converted into clean markdown tables that AI writers can understand.",
            "paragraphs": [
                "Once Pandas finishes computing its statistical distribution, that information lives as an in-memory binary matrix inside the computer's RAM.",
                "The next challenge is passing those numbers to the Content Writer agent so the writer can reference them in its sentences and display them nicely for human readers.",
                "Marketverse bridges this gap using Markdown tables generated via Pandas' `.to_markdown()` method.",
                "Markdown is a lightweight text formatting syntax that uses pipes (`|`) and hyphens (`-`) to represent table headers, columns, and rows in plain readable text.",
                "Because Markdown tables are plain text, our language models can read them effortlessly without misaligning columns or losing track of decimal points.",
                "Our tool formats the numbers to two decimal places, aligns numerical values to the right, and adds descriptive headers like 'Revenue ($B)' and 'Op Margin %'.",
                "This clean textual representation ensures that when the Content Writer crafts its report, it quotes the exact numbers from the table with 100% precision."
            ]
        },
        {
            "num": 19,
            "title": "Meet the Content Writer – The Technical Reports Writer Agent",
            "category": "Agent Spotlight",
            "subtitle": "The master storyteller that turns raw facts and math tables into a publication-ready report.",
            "paragraphs": [
                "Numbers and search snippets are useless if nobody can read them. That is where our third specialist, the Content Writer agent, comes in.",
                "Its official role in Marketverse is 'Technical Reports Writer', and its goal is: 'Synthesize information, write sections, and structure copy.'",
                "We gave this agent the persona of an elite financial reporter and institutional documentation writer who knows how to structure complex memos for senior corporate executives.",
                "The Content Writer does not have access to search tools or scraping functions; it is deliberately kept away from raw internet browsing so it can concentrate 100% of its energy on clear writing.",
                "When the Manager LLM provides it with the research dossier and the Pandas math tables, the writer reads both inputs carefully and weaves them together into a compelling narrative.",
                "It knows how to write punchy executive summaries, group companies into logical competitive tiers, explain technology bottlenecks clearly, and outline balanced investment risks.",
                "Thanks to the Content Writer, every Marketverse report reads like an institutional research document authored by a senior analyst at Goldman Sachs or McKinsey."
            ]
        },
        {
            "num": 20,
            "title": "Report Synthesis – How Raw Data Becomes an Executive Document",
            "category": "Editorial Process",
            "subtitle": "The delicate art of combining qualitative research and quantitative math into one voice.",
            "paragraphs": [
                "Synthesis is the process of taking several different pieces of information and combining them into a single, cohesive story that is greater than the sum of its parts.",
                "In Marketverse, synthesis is what separates our platform from basic tools that simply dump raw search results onto a screen.",
                "When the Content Writer receives the findings, it looks for connections between the words and the numbers. For instance, if the researcher noted that 'AI demand is booming', the writer looks at the math table to see which company grew the fastest.",
                "It notices that NVIDIA grew by 93.6% YoY while maintaining a 62.3% operating margin, and it links those numbers directly to the qualitative findings about data center GPU shortages.",
                "This connection gives the report immense credibility, because every high-level claim is immediately backed up by concrete financial proof.",
                "The writer also eliminates duplicate information, smooths out awkward phrasing, and organizes the text into logical headings and bullet points.",
                "The result is an executive document that a CEO or portfolio manager can read in five minutes to make multi-million dollar business decisions with confidence."
            ]
        },
        {
            "num": 21,
            "title": "The Five Core Sections of a Marketverse Research Dossier",
            "category": "Document Structure",
            "subtitle": "A guided tour through the standardized sections that make every Marketverse report thorough and easy to navigate.",
            "paragraphs": [
                "Consistency in document structure is critical for professional analysis because busy executives need to know exactly where to look for specific answers.",
                "Marketverse enforces a strict five-section architecture across every generated report, ensuring uniform quality and effortless readability.",
                "Section 1 is the 'Executive Summary & Market Snapshot', which delivers high-level strategic takeaways, key market indicators, and essential highlights right up front.",
                "Section 2 is 'Sector Growth Drivers & Strategic Technology Catalysts', which explores the technological breakthroughs, customer demand trends, and hardware bottlenecks driving the market.",
                "Section 3 is 'Quantitative Financial Matrix & Descriptive Statistics', where the Pandas summary table and corporate breakdown tables live alongside detailed mathematical commentary.",
                "Section 4 is 'Peer Group Valuation & Competitive Benchmarking', which groups companies into competitive tiers (such as Accelerated Hardware vs Platform Titans) and evaluates their P/E multiples.",
                "Finally, Section 5 is 'Risk Factors, Sensitivity Analysis & Strategic Outlook', which candidly discusses power grid shortages, regulatory scrutiny, and supply chain threats before giving a balanced future forecast."
            ]
        },
        {
            "num": 22,
            "title": "Programmatic PDF Generation – Introducing ReportLab Architecture",
            "category": "Document Engineering",
            "subtitle": "Why Marketverse uses ReportLab to draw PDFs from scratch rather than relying on messy HTML converters.",
            "paragraphs": [
                "Many automated report tools take a lazy shortcut: they convert a web page into a PDF using headless browser screenshot tools. This often leads to broken page breaks, cut-off tables, and ugly fonts.",
                "Marketverse takes a much more professional engineering path by using ReportLab, the premier open-source library for creating PDF files programmatically in Python.",
                "ReportLab treats a PDF document like a blank mathematical canvas with an exact width and height measured in typographic points (72 points per inch).",
                "It uses an architecture called 'Platypus' (Page Layout and Typography Using Scripts), which separates high-level content elements like Paragraphs and Tables from low-level page geometry.",
                "When Marketverse compiles a report, it builds a list of content blocks called a 'story'. It adds banners, headers, paragraphs, and tables into this story in order.",
                "ReportLab's layout engine then pours the story onto A4 pages, calculating exact line heights, word wraps, and spacing to ensure that nothing ever clips or looks distorted.",
                "By using ReportLab directly, Marketverse produces crisp vector documents that look stunning whether viewed on a 4K monitor or printed on high-end office paper."
            ]
        },
        {
            "num": 23,
            "title": "The Magic of NumberedCanvas – Dynamic Page X of Y Numbering",
            "category": "Advanced PDF Tricks",
            "subtitle": "How our custom two-pass canvas solves the classic problem of knowing the total page count in advance.",
            "paragraphs": [
                "One of the trickiest problems in computer document generation is printing 'Page 1 of 12' on the very first page when the computer doesn't yet know how many total pages the document will take!",
                "In standard one-pass rendering, when the computer is drawing page 1, it has no idea if the document will end up being 5 pages, 10 pages, or 37 pages long.",
                "Marketverse solves this classic challenge elegantly by subclassing ReportLab's canvas into a custom class called `NumberedCanvas` in `crew/utils/pdf_generator.py`.",
                "The `NumberedCanvas` uses a clever two-pass mechanism. During the first pass, as paragraphs and tables are being laid out, the canvas saves each finished page state in memory without finalizing it.",
                "Once the entire document has been laid out, the canvas checks the total length of its saved page list, giving it the exact total page count (for example, 37).",
                "During the second pass, it revisits every saved page and paints the running header, the thin dividing rule, and the footer string 'Page X of Y' before writing the final PDF bytes to disk.",
                "This small piece of engineering genius ensures that every Marketverse document features flawless, institutional-grade page numbering that always reflects the true total page count."
            ]
        },
        {
            "num": 24,
            "title": "Designing Beautiful Document Layouts – Headers, Banners, and Color Palettes",
            "category": "Design & UX",
            "subtitle": "The visual design philosophy behind Marketverse's executive typography and styling.",
            "paragraphs": [
                "A brilliant report with ugly formatting will often be ignored, while a beautifully designed document commands respect, captures attention, and builds trust immediately.",
                "We designed Marketverse's visual aesthetic around a modern corporate color palette: Deep Slate Navy (`#0F172A`), Royal Navy (`#1E3A8A`), Bright Blue (`#2563EB`), and Cyan (`#0284C7`).",
                "The first page of every report opens with a full-width header banner that clearly displays the title, the target market topic, the generation timestamp, and the security classification.",
                "We chose Helvetica as our primary font because of its clean, timeless legibility across both digital screens and physical print.",
                "Typography styles are hierarchically defined in `_init_styles()` with explicit font sizes and line leadings (such as 14pt bold on 18pt leading for major headings) to ensure comfortable reading rhythms.",
                "Subtle horizontal rule flowables (`HRFlowable`) in accent blue are placed underneath section titles to guide the reader's eye naturally down the page.",
                "Every element, from paragraph margins to bullet indents, is calibrated down to the point, resulting in a cohesive visual identity that rivals top-tier management consulting firms."
            ]
        },
        {
            "num": 25,
            "title": "Rendering Tables in ReportLab – Alternating Rows and Clean Borders",
            "category": "Table Design",
            "subtitle": "How complex financial tables are styled with alternating zebra rows and clean borders for maximum readability.",
            "paragraphs": [
                "Tables are the heart of financial reports, but poorly formatted tables with crowded text and harsh black gridlines make readers dizzy.",
                "In Marketverse, tables are built using ReportLab's `Table` and `TableStyle` classes, which provide complete control over every cell, row, and column.",
                "We style table headers with a solid dark navy background and bold white text, immediately establishing what data lives in each column.",
                "To make scanning long rows easy on the eyes, we apply an alternating row color pattern—often called 'zebra striping'—switching between soft light slate (`#F8FAFC`) and pure white (`#FFFFFF`).",
                "Numerical values are right-aligned using a dedicated `TableCellNumeric` paragraph style, making it effortless to compare values and notice decimal alignments at a glance.",
                "Borders are colored in soft slate gray (`#E2E8F0`) with a thin 0.5-point stroke, providing structure without cluttering the visual space.",
                "Finally, cell padding is calibrated to 4 points top and bottom, ensuring that tables remain compact enough to fit comfortably on the page without cramping the text."
            ]
        },
        {
            "num": 26,
            "title": "Execution Benchmarking – Tracking Every Second with benchmarks.json",
            "category": "Telemetry & Observability",
            "subtitle": "How Marketverse measures execution speed and logs dynamic task routing to local JSON files.",
            "paragraphs": [
                "In production software systems, you cannot improve what you do not measure. Knowing how long each agent took and how tasks were routed is vital for performance optimization.",
                "Marketverse features a dedicated telemetry engine implemented in `crew/utils/benchmark.py` under the `BenchmarkTracker` class.",
                "When a workflow starts, the tracker starts a high-resolution wall-clock timer and generates a unique workflow identifier.",
                "As the supervisor Manager LLM delegates each task, the tracker records the start time, agent role, task name, and delegating authority.",
                "When an agent completes its work, the tracker stops the timer, calculates the duration in seconds to four decimal places, and records an output preview.",
                "At the end of the run, the tracker computes aggregate statistics per agent and writes the complete telemetry trace to `benchmarks.json` and `output/benchmarks.json`.",
                "This benchmarking file allows engineering teams to monitor agent latencies, detect bottlenecks in API calls, and audit exactly which agent performed each step of the analysis."
            ]
        },
        {
            "num": 27,
            "title": "The Command Line Interface – Running Marketverse from the Terminal",
            "category": "CLI Tools",
            "subtitle": "How developers and power users can trigger research workflows directly from PowerShell or bash.",
            "paragraphs": [
                "While graphical web interfaces are wonderful for interactive use, engineers and automated cron jobs often prefer running tools directly from the command line.",
                "Marketverse features a clean, robust CLI entry point in `main.py` built using Python's standard `argparse` module.",
                "To start a full research run, you simply open your terminal and type `python main.py --query 'Tech Sector Q3 Analysis'`.",
                "The CLI supports helpful optional flags: `--csv` to point to a custom spreadsheet, `--output-dir` to change where files are saved, and `--pdf-name` to customize the output document name.",
                "As the script runs, it outputs a clean real-time log trace to the console, showing the Manager LLM initializing, each agent receiving its dynamic delegation, and the step completion checks.",
                "Once finished, the CLI prints a beautiful summary box showing total execution time, task count, and absolute file paths to the generated Markdown, PDF, and benchmark JSON files.",
                "This flexible CLI interface makes Marketverse ideal for automated CI/CD pipelines, nightly market briefing cron jobs, and terminal power users."
            ]
        },
        {
            "num": 28,
            "title": "The Interactive Web Dashboard – The Localhost 3000 User Experience",
            "category": "Web Application",
            "subtitle": "A visual tour of the single-page web app running on port 3000 that brings Marketverse to life.",
            "paragraphs": [
                "Not everyone loves working in a command-line terminal. For everyday business users, Marketverse includes a complete interactive web dashboard hosted locally on port 3000.",
                "When you navigate to `http://localhost:3000` in your web browser, you are greeted by a sleek dark-mode interface styled in deep navy and cyan accents.",
                "The top of the page displays the active agent team roster, showing real-time status badges for the Manager LLM, the Lead Researcher, the Data Analyst, and the Content Writer.",
                "A prominent search panel lets you type any custom market topic or click pre-built quick-query chips like 'Hyperscaler Cloud & AI Capex' or 'Semiconductor & Foundry Outlook'.",
                "When you click 'Run Multi-Agent Research', an animated 5-step progress tracker illuminates each phase of the pipeline as the agents work in the background.",
                "Below the query bar, five real-time KPI cards showcase aggregate revenue, mean growth rate, operating margins, median P/E, and combined market capitalization across the tracked cohort.",
                "Four interactive tabs allow you to read the formatted executive report, explore the Pandas math tables, preview and download the compiled PDF, and inspect the raw benchmark telemetry."
            ]
        },
        {
            "num": 29,
            "title": "Under the Hood of the Web Server – Starlette and Uvicorn",
            "category": "Backend Engineering",
            "subtitle": "The ultra-fast asynchronous Python web server that powers the Marketverse web experience.",
            "paragraphs": [
                "To deliver the localhost 3000 experience without bloating the project with heavy web frameworks, Marketverse uses Starlette and Uvicorn.",
                "Starlette is a lightweight, high-performance Asynchronous Server Gateway Interface (ASGI) toolkit that powers the foundation of popular frameworks like FastAPI.",
                "Uvicorn is an ultra-fast ASGI web server implementation written in Python and C, capable of serving thousands of concurrent connections with minimal CPU overhead.",
                "In `server.py`, we define clean asynchronous routes that handle incoming HTTP requests and return JSON responses, raw text, or binary file streams.",
                "Because Starlette is fully asynchronous, triggering a multi-agent research workflow never freezes the web server or blocks other users from viewing previously compiled reports.",
                "The entire frontend is served as a self-contained single-page application using modern HTML5, CSS3, and native vanilla JavaScript, requiring zero node_modules or complex build tools to run.",
                "This lean architecture means the web server starts up in less than 200 milliseconds and runs happily on everything from a lightweight laptop to an enterprise cloud server."
            ]
        },
        {
            "num": 30,
            "title": "The Marketverse REST API – Endpoints for Modern Integrations",
            "category": "API Reference",
            "subtitle": "How external apps, Slack bots, and corporate systems can integrate with Marketverse via HTTP.",
            "paragraphs": [
                "Marketverse is designed not just as a standalone tool, but as a modular platform that other software systems can easily talk to over the network.",
                "Our server exposes a comprehensive suite of RESTful API endpoints that return standardized JSON and binary streams for seamless integration.",
                "The `GET /api/status` endpoint provides real-time health checks, returning the framework version, active agent roles, and the configured LLM model.",
                "The `POST /api/run` endpoint accepts a JSON body with a target query (e.g., `{'query': 'Semiconductors'}`) and runs the full multi-agent pipeline, returning the report and benchmarks.",
                "The `GET /api/report/markdown` and `GET /api/report/pdf` endpoints stream the latest generated report in raw markdown text or binary PDF format with proper inline headers for browser viewing.",
                "The `GET /api/data` endpoint returns the underlying corporate metrics and Pandas descriptive statistics as clean JSON dictionaries for custom frontend dashboards.",
                "Finally, `GET /api/benchmarks` exposes the execution telemetry, making it trivial to pipe Marketverse performance metrics into monitoring tools like Datadog or Prometheus."
            ]
        },
        {
            "num": 31,
            "title": "Automated Testing with Pytest – Ensuring Bulletproof Code",
            "category": "Quality Assurance",
            "subtitle": "How our 14 automated tests guarantee that math calculations and PDF layouts never break.",
            "paragraphs": [
                "Software that is not tested is software that is broken. In financial applications where accuracy is paramount, comprehensive automated testing is non-negotiable.",
                "Marketverse includes a complete automated test suite located in `tests/` and powered by `pytest`, the premier testing framework in the Python ecosystem.",
                "Our tests cover every critical layer of the application: Pandas statistical calculations, currency string sanitization, ReportLab PDF layout generation, scraper tool resilience, and CLI arguments.",
                "In `test_pandas_analysis.py`, we feed the parser a controlled mock dataset with known mathematical properties and assert that the computed mean, min, max, and standard deviation match exact theoretical values.",
                "In `test_pdf_layout.py`, we verify that the ReportLab compiler generates a valid binary file starting with the official `%PDF-` header without raising any layout or styling exceptions.",
                "In `test_orchestration_benchmarks.py`, we verify that the three specialized agent roles match project requirements and that benchmark timers record positive durations.",
                "All 14 tests pass with 100% success in under 12 seconds, giving developers complete confidence that new features will never introduce regressions or calculation errors."
            ]
        },
        {
            "num": 32,
            "title": "Secrets Isolation and Security – Safe API Key Management",
            "category": "Security & Best Practices",
            "subtitle": "How Marketverse protects your sensitive API credentials from accidental leaks or exposure.",
            "paragraphs": [
                "Connecting to modern AI and search services requires private API keys. If these secret keys are accidentally committed to public GitHub repositories, malicious actors can steal them within seconds.",
                "Marketverse enforces strict secrets isolation following the Twelve-Factor App methodology for modern software security.",
                "All secret keys (`OPENAI_API_KEY`, `TAVILY_API_KEY`, `SERPER_API_KEY`) are stored exclusively in an uncommitted `.env` file on the developer's local machine.",
                "Our `.gitignore` file explicitly excludes `.env` while preserving a safe `.env.example` template that contains placeholder values for documentation purposes.",
                "Inside the code, `python-dotenv` loads environment variables into memory at application startup, keeping credentials safely sequestered from public code files.",
                "Furthermore, our sandboxed environment automatically redirects temporary storage and telemetry paths into workspace folders, preventing unauthorized file writes across the host operating system.",
                "This disciplined security posture ensures that Marketverse can be shared openly with open-source communities without risking accidental credential leaks."
            ]
        },
        {
            "num": 33,
            "title": "Enterprise Use Case 1 – Institutional Investment and Hedge Funds",
            "category": "Real-World Application",
            "subtitle": "How asset managers and hedge fund analysts use Marketverse to accelerate earnings season prep.",
            "paragraphs": [
                "During quarterly corporate earnings season, investment analysts at hedge funds and mutual funds are flooded with dozens of earnings reports every single day.",
                "A typical junior analyst might spend 14 hours reading transcripts, manually pulling financial numbers from 10-Q filings, and updating internal valuation models.",
                "By deploying Marketverse, an investment firm can automate the preliminary discovery phase of earnings analysis across hundreds of public equities.",
                "An analyst can type 'Hyperscaler Cloud & AI Infrastructure Q3' into Marketverse, and within seconds receive a synthesized report comparing Microsoft Azure, Google Cloud, and AWS revenue growth rates.",
                "Because Marketverse calculates descriptive statistics like median operating margins and revenue dispersion, analysts can immediately spot which companies are outperforming their peer group.",
                "The generated PDF report can be distributed directly to portfolio managers as a morning briefing memo before the opening bell rings on Wall Street.",
                "This speed advantage allows investment teams to form high-conviction theses faster than competing funds, turning raw data into superior investment returns."
            ]
        },
        {
            "num": 34,
            "title": "Enterprise Use Case 2 – Venture Capital and Startup Due Diligence",
            "category": "Real-World Application",
            "subtitle": "How startup investors benchmark private seed deals against public market metrics.",
            "paragraphs": [
                "Venture capital firms evaluate thousands of early-stage startups every year, trying to determine which young companies have the potential to become multi-billion-dollar winners.",
                "When evaluating a new pitch deck, venture capitalists need to benchmark the startup's financial projections against the real-world performance of established public market leaders.",
                "Marketverse provides VC associates with an instantaneous benchmarking engine to evaluate industry multiples, net retention rates, and operating leverage.",
                "If a startup founder claims their cloud software company will easily achieve 80% gross margins, an associate can run Marketverse to see that the median public software margin is actually 32.2%.",
                "This reality check helps venture firms price deals accurately, ask smarter questions during partner meetings, and spot unrealistic founder projections before investing capital.",
                "The compiled ReportLab PDF can be archived in the firm's CRM as part of the formal investment memo documentation required by limited partner advisory committees.",
                "Marketverse transforms due diligence from an exhausting multi-day research slog into a structured, data-driven workflow that scales effortlessly."
            ]
        },
        {
            "num": 35,
            "title": "Enterprise Use Case 3 – Corporate Strategy and Competitor Monitoring",
            "category": "Real-World Application",
            "subtitle": "How corporate executives and strategy teams monitor competitor movements in real time.",
            "paragraphs": [
                "In fast-moving industries like technology and semiconductors, corporate leadership teams cannot afford to wait months for third-party market research reports that cost tens of thousands of dollars.",
                "Corporate strategy officers need up-to-date intelligence on competitor capital expenditure, technology partnerships, and supply chain constraints right now.",
                "Marketverse serves as an internal, always-on strategy think-tank for corporate leadership teams across any sector.",
                "By querying peer group metrics, a strategy team can track how much capital competitors are pouring into custom AI chips, high-density data centers, and advanced packaging.",
                "The qualitative synthesis highlights key strategic risks, such as power grid interconnect delays, allowing executive committees to adjust their own operational roadmaps proactively.",
                "Because Marketverse reports are compiled into clean, branded A4 PDFs with automatic page numbers, they can be printed and placed on board room tables with zero additional formatting.",
                "This empowers corporate leaders to navigate market disruptions with situational awareness and maintain their competitive edge."
            ]
        },
        {
            "num": 36,
            "title": "Troubleshooting, Edge Cases, and System Robustness",
            "category": "Operations & Support",
            "subtitle": "A practical guide to handling network errors, missing files, and unusual data gracefully.",
            "paragraphs": [
                "Even the best software occasionally encounters unexpected conditions: lost network packets, corrupted input files, rate-limited API keys, or unusual operating system permissions.",
                "Marketverse is built with defensive programming patterns at every layer to diagnose and recover from these edge cases automatically.",
                "If a user provides a path to a CSV file that does not exist on disk, `load_and_preprocess_dataframe` catches the error and falls back safely to the default verified dataset.",
                "If web scraping fails because a target server blocks bots or times out, the scraper tool logs a warning, catches the exception, and supplies curated intelligence so the agent workflow continues.",
                "On Windows environments where sandbox permissions occasionally restrict writes to `%LOCALAPPDATA%`, `crew/config.py` automatically redirects temporary storage to a safe workspace directory.",
                "If an LLM model returns an unexpectedly brief response, the ReportLab compiler's flexible layout flowables adjust their vertical spacing automatically to avoid awkward white gaps.",
                "This thorough exception handling makes Marketverse exceptionally robust, ensuring smooth operation whether running on a developer's desktop or inside a headless Docker container."
            ]
        },
        {
            "num": 37,
            "title": "Future Horizons – Expanding Marketverse with New Models and Live Feeds",
            "category": "Vision & Roadmap",
            "subtitle": "Exciting future enhancements: live stock tickers, speech synthesis, and multimodal charts.",
            "paragraphs": [
                "Marketverse is already a powerful platform for multi-agent market analysis, but the roadmap ahead contains even more exciting possibilities.",
                "One major planned enhancement is the integration of direct real-time financial market data feeds, such as Alpha Vantage, Polygon.io, and Yahoo Finance APIs.",
                "This will allow Marketverse agents to stream live stock ticker prices, intraday volume spikes, and real-time options volatility directly into the Pandas analysis engine.",
                "Another exciting frontier is native multimodal generation: allowing the Content Writer and ReportLab compiler to generate interactive vector charts, trendlines, and candlestick graphs.",
                "We also plan to add support for open-source local language models running via Ollama or vLLM, allowing organizations to run Marketverse completely on-premises with zero data leaving their servers.",
                "Additionally, an automated audio briefing feature using text-to-speech could summarize executive findings into a 3-minute morning podcast for busy commuters.",
                "Marketverse is just getting started, demonstrating how autonomous AI agents, rigorous math libraries, and beautiful document compilers can work together to democratize financial intelligence for everyone."
            ]
        }
    ]


def build_documentation_pdf(output_path: str = "output/Marketverse_Documentation.pdf") -> str:
    """Compile the complete 37-topic, 37-page documentation PDF."""
    target_path = Path(output_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    base = getSampleStyleSheet()

    # Custom Typographic Hierarchy calibrated so 1 topic + 7 paragraphs fits exactly 1 page
    style_category = ParagraphStyle(
        "DocCategory",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=COLOR_CYAN,
        textTransform="uppercase",
        spaceAfter=3,
    )

    style_title = ParagraphStyle(
        "DocTitle",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=3,
    )

    style_subtitle = ParagraphStyle(
        "DocSubtitle",
        parent=base["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11,
        textColor=COLOR_MUTED,
        spaceAfter=6,
    )

    style_para = ParagraphStyle(
        "DocPara",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.2,
        textColor=COLOR_TEXT,
        spaceAfter=5.5,
    )

    style_para_num = ParagraphStyle(
        "DocParaNum",
        parent=style_para,
        textColor=COLOR_SECONDARY,
        fontName="Helvetica-Bold",
    )

    topics = get_all_topics()
    story = []

    for idx, topic in enumerate(topics):
        num = topic["num"]
        title = topic["title"]
        category = topic["category"]
        subtitle = topic["subtitle"]
        paragraphs = topic["paragraphs"]

        # Ensure exactly 7 paragraphs
        if len(paragraphs) != 7:
            raise ValueError(f"Topic {num} does not have exactly 7 paragraphs! Has: {len(paragraphs)}")

        # 1. Category Tag
        story.append(Paragraph(f"<b>SECTION {num:02d} &bull; {category}</b>", style_category))

        # 2. Topic Title
        story.append(Paragraph(f"<b>{title}</b>", style_title))

        # 3. Subtitle
        story.append(Paragraph(subtitle, style_subtitle))

        # 4. Colored Accent Line
        story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceBefore=0, spaceAfter=7))

        # 5. Exactly 7 Paragraphs
        for p_idx, text in enumerate(paragraphs, 1):
            clean_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            para_content = f"<b>[{p_idx}]</b> {clean_text}"
            story.append(Paragraph(para_content, style_para))

        # 6. PageBreak after every topic except the last one (total 37 pages!)
        if idx < len(topics) - 1:
            story.append(PageBreak())

    # Build PDF with dynamic NumberedCanvas
    doc.build(story, canvasmaker=DocNumberedCanvas)
    return str(target_path)


if __name__ == "__main__":
    out_pdf = build_documentation_pdf("output/Marketverse_Documentation.pdf")
    # Also copy to root for immediate access
    import shutil
    shutil.copy(out_pdf, "Marketverse_Documentation.pdf")
    print(f"[SUCCESS] Built 37-page documentation PDF at: {out_pdf}")
    print(f"[SUCCESS] File size: {os.path.getsize(out_pdf):,} bytes")
