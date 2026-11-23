"""Marketverse Localhost 3000 Web Application & API Server.

Provides a modern interactive dashboard and REST API for Marketverse
hierarchical multi-agent research, Pandas financial matrix analytics,
benchmarks visualization, and ReportLab PDF document preview/download.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

# Ensure workspace root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import crew.config  # Initializes sandboxed environment and loads .env
from crew.crew import MarketverseCrew
from crew.utils.pdf_generator import compile_pdf_report
from crew.tools.financial_tool import (
    load_and_preprocess_dataframe,
    get_financial_summary_stats,
    DEFAULT_CSV_PATH
)

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, FileResponse, HTMLResponse, Response
from starlette.requests import Request
import uvicorn


async def api_status(request: Request) -> JSONResponse:
    """Return system status and active agent configuration."""
    return JSONResponse({
        "status": "ONLINE",
        "app_name": "Marketverse",
        "version": "1.0.0",
        "framework": "CrewAI",
        "process_mode": "Process.hierarchical",
        "manager_llm": os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
        "agents": [
            {"role": "Market Research Specialist", "title": "Lead Researcher", "status": "READY"},
            {"role": "Financial Data Analyst", "title": "Data Analyst", "status": "READY"},
            {"role": "Technical Reports Writer", "title": "Content Writer", "status": "READY"}
        ],
        "pdf_engine": "ReportLab A4 (NumberedCanvas)",
        "pandas_version": "Available"
    })


async def api_run(request: Request) -> JSONResponse:
    """Run Marketverse hierarchical multi-agent research workflow."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    query = body.get("query", "Tech Sector Q3 Analysis").strip()
    if not query:
        query = "Tech Sector Q3 Analysis"

    csv_path = body.get("csv_path", str(DEFAULT_CSV_PATH))

    # Run Crew
    orchestrator = MarketverseCrew(query=query, csv_path=csv_path)
    result = orchestrator.kickoff()
    markdown_report = result["markdown_report"]

    # Save Markdown
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "market_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    # Compile PDF
    pdf_path = output_dir / "market_report.pdf"
    compile_pdf_report(markdown_report, str(pdf_path), query=query, csv_path=csv_path)

    return JSONResponse({
        "success": True,
        "query": query,
        "duration_seconds": result["benchmarks"]["total_duration_seconds"],
        "markdown_report": markdown_report,
        "benchmarks": result["benchmarks"],
        "pdf_url": "/api/report/pdf",
        "markdown_url": "/api/report/markdown"
    })


async def api_report_markdown(request: Request) -> Response:
    """Serve latest markdown report."""
    md_path = BASE_DIR / "output" / "market_report.md"
    if not md_path.exists():
        md_path = BASE_DIR / "output" / "sample_market_report.md"

    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, media_type="text/markdown")
    return JSONResponse({"error": "No report found. Run analysis first."}, status_code=404)


async def api_report_pdf(request: Request) -> Response:
    """Stream latest ReportLab compiled A4 PDF report."""
    pdf_path = BASE_DIR / "output" / "market_report.pdf"
    if not pdf_path.exists():
        pdf_path = BASE_DIR / "output" / "sample_market_report.pdf"

    if pdf_path.exists():
        return FileResponse(
            str(pdf_path),
            media_type="application/pdf",
            headers={"Content-Disposition": 'inline; filename="market_report.pdf"'}
        )
    return JSONResponse({"error": "No PDF report found. Run analysis first."}, status_code=404)


async def api_benchmarks(request: Request) -> JSONResponse:
    """Return execution benchmarks JSON."""
    json_path = BASE_DIR / "benchmarks.json"
    if not json_path.exists():
        json_path = BASE_DIR / "output" / "benchmarks.json"

    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(data)
    return JSONResponse({"error": "No benchmarks logged yet."}, status_code=404)


async def api_data(request: Request) -> JSONResponse:
    """Return raw financial dataset and summary stats."""
    try:
        df = load_and_preprocess_dataframe(str(DEFAULT_CSV_PATH))
        peers = df.to_dict(orient="records")
        summary_df = get_financial_summary_stats(df).reset_index()
        summary_df.rename(columns={"index": "statistic"}, inplace=True)
        summary = summary_df.to_dict(orient="records")

        kpis = {
            "total_revenue": round(df["Revenue_Billions"].sum(), 2) if "Revenue_Billions" in df.columns else 0,
            "mean_growth": round(df["YoY_Growth_Pct"].mean(), 1) if "YoY_Growth_Pct" in df.columns else 0,
            "mean_margin": round(df["Operating_Margin_Pct"].mean(), 1) if "Operating_Margin_Pct" in df.columns else 0,
            "median_pe": round(df["PE_Ratio"].median(), 1) if "PE_Ratio" in df.columns else 0,
            "total_market_cap": round(df["Market_Cap_Billions"].sum(), 2) if "Market_Cap_Billions" in df.columns else 0,
            "companies_count": len(df)
        }

        return JSONResponse({
            "kpis": kpis,
            "peers": peers,
            "summary_stats": summary
        })
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Marketverse | Multi-Agent Market Research & Analytics Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0B0F19;
      --card-bg: #111827;
      --card-border: #1F2937;
      --primary: #3B82F6;
      --primary-hover: #2563EB;
      --accent: #06B6D4;
      --text: #F3F4F6;
      --text-muted: #9CA3AF;
      --success: #10B981;
      --warning: #F59E0B;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 50px;
    }
    header {
      background: rgba(17, 24, 39, 0.95);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(12px);
    }
    .header-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-badge {
      background: linear-gradient(135deg, #2563EB, #06B6D4);
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 20px;
      color: white;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }
    .brand-title {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #FFFFFF, #93C5FD);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-subtitle {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }
    .nav-badges {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.1);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10B981;
      box-shadow: 0 0 8px #10B981;
    }
    .btn-pdf {
      background: linear-gradient(135deg, #2563EB, #1D4ED8);
      color: white;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn-pdf:hover {
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.5);
      transform: translateY(-1px);
    }
    main {
      max-width: 1400px;
      margin: 24px auto;
      padding: 0 24px;
    }
    /* Agent Roster Bar */
    .roster-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .roster-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
      overflow: hidden;
    }
    .roster-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
    }
    .roster-role {
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--accent);
      letter-spacing: 0.5px;
    }
    .roster-name {
      font-size: 15px;
      font-weight: 700;
      color: white;
    }
    .roster-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.4;
    }
    /* Query Runner Bar */
    .search-panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    .search-label {
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 10px;
      display: block;
    }
    .search-box {
      display: flex;
      gap: 12px;
    }
    .search-input {
      flex: 1;
      background: #0B0F19;
      border: 1px solid #374151;
      border-radius: 8px;
      padding: 14px 18px;
      font-size: 15px;
      color: white;
      outline: none;
      transition: border-color 0.2s;
    }
    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }
    .btn-run {
      background: linear-gradient(135deg, #2563EB, #06B6D4);
      color: white;
      border: none;
      padding: 14px 28px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }
    .btn-run:hover {
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
      transform: translateY(-1px);
    }
    .btn-run:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .quick-queries {
      display: flex;
      gap: 8px;
      margin-top: 12px;
      flex-wrap: wrap;
      align-items: center;
    }
    .quick-title {
      font-size: 12px;
      color: var(--text-muted);
      margin-right: 4px;
    }
    .query-tag {
      background: #1F2937;
      color: #93C5FD;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      border: 1px solid #374151;
      transition: all 0.2s;
    }
    .query-tag:hover {
      background: #2563EB;
      color: white;
      border-color: #2563EB;
    }
    /* Execution Pipeline Trace */
    .pipeline-progress {
      display: none;
      background: #0D1526;
      border: 1px solid #1E3A8A;
      border-radius: 10px;
      padding: 16px;
      margin-top: 16px;
    }
    .progress-steps {
      display: flex;
      justify-content: space-between;
      position: relative;
    }
    .step-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
    }
    .step-item.active {
      color: #38BDF8;
    }
    .step-item.done {
      color: #34D399;
    }
    .step-icon {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #1E293B;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
    }
    /* KPI Metric Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
    }
    .kpi-label {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 6px;
    }
    .kpi-value {
      font-size: 24px;
      font-weight: 800;
      color: white;
      letter-spacing: -0.5px;
    }
    .kpi-sub {
      font-size: 11px;
      color: #34D399;
      margin-top: 4px;
    }
    /* Tab Controls */
    .tabs-nav {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 20px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 12px 20px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn:hover {
      color: white;
    }
    .tab-btn.active {
      color: #38BDF8;
      border-bottom-color: #38BDF8;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    /* Tables */
    .table-container {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow-x: auto;
      margin-bottom: 24px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }
    thead {
      background: #0F172A;
      border-bottom: 1px solid var(--card-border);
    }
    th {
      padding: 12px 16px;
      font-weight: 700;
      color: #93C5FD;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
    }
    td {
      padding: 12px 16px;
      border-bottom: 1px solid #1F2937;
      color: var(--text);
    }
    tbody tr:hover {
      background: rgba(30, 41, 59, 0.5);
    }
    .num-col {
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
    }
    /* Report Viewer */
    .report-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 32px;
      line-height: 1.7;
    }
    .report-card h1 { font-size: 24px; color: white; margin-bottom: 16px; border-bottom: 2px solid var(--primary); padding-bottom: 10px; }
    .report-card h2 { font-size: 18px; color: #93C5FD; margin: 24px 0 12px; }
    .report-card h3 { font-size: 15px; color: #38BDF8; margin: 16px 0 8px; }
    .report-card p { margin-bottom: 14px; color: #E5E7EB; }
    .report-card ul { margin-left: 20px; margin-bottom: 14px; }
    .report-card li { margin-bottom: 6px; }
    .report-card hr { border: none; border-top: 1px solid var(--card-border); margin: 24px 0; }
    /* PDF Viewer Embed */
    .pdf-embed-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .pdf-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    iframe.pdf-frame {
      width: 100%;
      height: 800px;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      background: white;
    }
    /* Benchmarks View */
    .benchmark-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }
    .bench-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
    }
    .bench-title {
      font-size: 15px;
      font-weight: 700;
      color: white;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    pre.json-box {
      background: #0B0F19;
      border: 1px solid #1F2937;
      border-radius: 8px;
      padding: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: #38BDF8;
      overflow-x: auto;
      max-height: 400px;
    }
    @media (max-width: 1024px) {
      .roster-grid, .kpi-grid { grid-template-columns: repeat(2, 1fr); }
      .benchmark-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-container">
      <div class="brand">
        <div class="logo-badge">M</div>
        <div>
          <div class="brand-title">MARKETVERSE</div>
          <div class="brand-subtitle">Hierarchical Multi-Agent Market Intelligence</div>
        </div>
      </div>
      <div class="nav-badges">
        <div class="badge">
          <span class="badge-dot"></span>
          <span>Process.hierarchical Active</span>
        </div>
        <a href="/api/report/pdf" target="_blank" class="btn-pdf">
          <span>📄 View Typeset PDF</span>
        </a>
      </div>
    </div>
  </header>

  <main>
    <!-- Agent Team Roster -->
    <div class="roster-grid">
      <div class="roster-card">
        <span class="roster-role">Supervisor Manager</span>
        <span class="roster-name">Manager LLM (GPT-4o)</span>
        <span class="roster-desc">Dynamically assigns tasks, routes data, and verifies numerical integrity.</span>
      </div>
      <div class="roster-card">
        <span class="roster-role">Lead Researcher</span>
        <span class="roster-name">Market Research Specialist</span>
        <span class="roster-desc">Queries search networks, gathers SEC filings, and scrapes web metrics.</span>
      </div>
      <div class="roster-card">
        <span class="roster-role">Data Analyst</span>
        <span class="roster-name">Financial Data Analyst</span>
        <span class="roster-desc">Parses data matrices using Pandas and verifies statistical consistency.</span>
      </div>
      <div class="roster-card">
        <span class="roster-role">Content Writer</span>
        <span class="roster-name">Technical Reports Writer</span>
        <span class="roster-desc">Synthesizes research and statistics into institutional market reports.</span>
      </div>
    </div>

    <!-- Query Execution Form -->
    <div class="search-panel">
      <label class="search-label" for="queryInput">Target Market Research Topic or Sector Query</label>
      <div class="search-box">
        <input type="text" id="queryInput" class="search-input" value="Tech Sector Q3 Analysis" placeholder="Enter market sector or company query...">
        <button id="runBtn" class="btn-run" onclick="triggerWorkflow()">
          <span id="runBtnIcon">⚡</span>
          <span id="runBtnText">Run Multi-Agent Research</span>
        </button>
      </div>
      <div class="quick-queries">
        <span class="quick-title">Quick Topics:</span>
        <span class="query-tag" onclick="setQuery('Tech Sector Q3 Analysis')">Tech Sector Q3 Analysis</span>
        <span class="query-tag" onclick="setQuery('Hyperscaler Cloud & AI Capex')">Hyperscaler Cloud & AI Capex</span>
        <span class="query-tag" onclick="setQuery('Semiconductor & Foundry Outlook')">Semiconductor & Foundry Outlook</span>
        <span class="query-tag" onclick="setQuery('Enterprise SaaS & Cybersecurity NRR')">Enterprise SaaS & Cybersecurity NRR</span>
      </div>

      <!-- Execution Progress -->
      <div id="pipelineProgress" class="pipeline-progress">
        <div class="progress-steps">
          <div id="step-1" class="step-item active"><span class="step-icon">1</span> Manager Delegating</div>
          <div id="step-2" class="step-item"><span class="step-icon">2</span> Researcher Scraping</div>
          <div id="step-3" class="step-item"><span class="step-icon">3</span> Pandas Analyzing</div>
          <div id="step-4" class="step-item"><span class="step-icon">4</span> Writer Structuring</div>
          <div id="step-5" class="step-item"><span class="step-icon">5</span> PDF Compiling</div>
        </div>
      </div>
    </div>

    <!-- KPI Metric Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">TOTAL TRACKED REVENUE</div>
        <div id="kpiRevenue" class="kpi-value">$505.86B</div>
        <div class="kpi-sub">Across 10 Public Titans</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">MEAN YOY GROWTH RATE</div>
        <div id="kpiGrowth" class="kpi-value">24.1%</div>
        <div class="kpi-sub">Range: 6.1% to 93.6%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">MEAN OPERATING MARGIN</div>
        <div id="kpiMargin" class="kpi-value">32.2%</div>
        <div class="kpi-sub">Median: 31.6%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">MEDIAN P/E MULTIPLE</div>
        <div id="kpiPE" class="kpi-value">33.8x</div>
        <div class="kpi-sub">Normalized NTM Multiples</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">COMBINED MARKET CAP</div>
        <div id="kpiMarketCap" class="kpi-value">$17.47T</div>
        <div class="kpi-sub">Enterprise Valuation Total</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-nav">
      <button class="tab-btn active" onclick="switchTab('reportTab', this)">📝 Executive Report</button>
      <button class="tab-btn" onclick="switchTab('dataTab', this)">📊 Pandas Financial Matrix</button>
      <button class="tab-btn" onclick="switchTab('pdfTab', this)">📑 PDF Document Preview</button>
      <button class="tab-btn" onclick="switchTab('benchmarkTab', this)">⏱️ Execution Benchmarks</button>
    </div>

    <!-- Tab 1: Executive Report -->
    <div id="reportTab" class="tab-content active">
      <div id="reportContent" class="report-card">
        Loading latest market research report...
      </div>
    </div>

    <!-- Tab 2: Pandas Financial Matrix -->
    <div id="dataTab" class="tab-content">
      <h3 style="margin-bottom: 12px; color: #93C5FD;">Table 1: Pandas Descriptive Statistics Distribution</h3>
      <div class="table-container">
        <table id="statsTable">
          <thead>
            <tr>
              <th>Statistic</th>
              <th class="num-col">Revenue ($B)</th>
              <th class="num-col">YoY Growth %</th>
              <th class="num-col">Op Margin %</th>
              <th class="num-col">Net Income ($B)</th>
              <th class="num-col">FCF ($B)</th>
              <th class="num-col">P/E</th>
              <th class="num-col">Market Cap ($B)</th>
            </tr>
          </thead>
          <tbody id="statsBody">
            <!-- Dynamic Data -->
          </tbody>
        </table>
      </div>

      <h3 style="margin-bottom: 12px; color: #93C5FD;">Table 2: Corporate Peer Group Baseline Metrics</h3>
      <div class="table-container">
        <table id="peersTable">
          <thead>
            <tr>
              <th>Company</th>
              <th>Ticker</th>
              <th class="num-col">Revenue ($B)</th>
              <th class="num-col">YoY Growth %</th>
              <th class="num-col">Op Margin %</th>
              <th class="num-col">Net Income ($B)</th>
              <th class="num-col">FCF ($B)</th>
              <th class="num-col">P/E</th>
              <th class="num-col">Market Cap ($B)</th>
            </tr>
          </thead>
          <tbody id="peersBody">
            <!-- Dynamic Data -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 3: PDF Document Preview -->
    <div id="pdfTab" class="tab-content">
      <div class="pdf-embed-box">
        <div class="pdf-actions">
          <div>
            <h3 style="color: white; font-size: 16px;">Typeset A4 PDF Market Report (ReportLab)</h3>
            <p style="color: var(--text-muted); font-size: 12px;">Compiled with custom NumberedCanvas ('Page X of Y'), corporate headers, and styled tables.</p>
          </div>
          <a href="/api/report/pdf" target="_blank" download="market_report.pdf" class="btn-pdf">
            <span>⬇️ Download PDF File</span>
          </a>
        </div>
        <iframe src="/api/report/pdf" class="pdf-frame"></iframe>
      </div>
    </div>

    <!-- Tab 4: Execution Benchmarks -->
    <div id="benchmarkTab" class="tab-content">
      <div class="benchmark-grid">
        <div class="bench-card">
          <div class="bench-title">⚡ Agent Task Routing History</div>
          <div class="table-container" style="max-height: 400px;">
            <table id="routingTable">
              <thead>
                <tr>
                  <th>Step</th>
                  <th>Agent Role</th>
                  <th>Task Name</th>
                  <th class="num-col">Duration (s)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="routingBody">
                <!-- Dynamic Data -->
              </tbody>
            </table>
          </div>
        </div>

        <div class="bench-card">
          <div class="bench-title">📋 Raw benchmarks.json Telemetry</div>
          <pre id="jsonPreview" class="json-box">Loading benchmarks telemetry...</pre>
        </div>
      </div>
    </div>

  </main>

  <script>
    function setQuery(q) {
      document.getElementById('queryInput').value = q;
    }

    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      el.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }

    async function loadData() {
      try {
        const res = await fetch('/api/data');
        const data = await res.json();
        
        // Populate KPIs
        if (data.kpis) {
          document.getElementById('kpiRevenue').innerText = `$${data.kpis.total_revenue}B`;
          document.getElementById('kpiGrowth').innerText = `${data.kpis.mean_growth}%`;
          document.getElementById('kpiMargin').innerText = `${data.kpis.mean_margin}%`;
          document.getElementById('kpiPE').innerText = `${data.kpis.median_pe}x`;
          document.getElementById('kpiMarketCap').innerText = `$${(data.kpis.total_market_cap / 1000).toFixed(2)}T`;
        }

        // Populate Stats Table
        const statsBody = document.getElementById('statsBody');
        statsBody.innerHTML = '';
        data.summary_stats.forEach(row => {
          statsBody.innerHTML += `
            <tr>
              <td><b>${row.statistic}</b></td>
              <td class="num-col">${row.Revenue_Billions?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.YoY_Growth_Pct?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.Operating_Margin_Pct?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.Net_Income_Billions?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.Free_Cash_Flow_Billions?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.PE_Ratio?.toFixed(2) || '-'}</td>
              <td class="num-col">${row.Market_Cap_Billions?.toFixed(2) || '-'}</td>
            </tr>
          `;
        });

        // Populate Peers Table
        const peersBody = document.getElementById('peersBody');
        peersBody.innerHTML = '';
        data.peers.forEach(p => {
          peersBody.innerHTML += `
            <tr>
              <td><b>${p.Company}</b></td>
              <td><span style="background: #1E3A8A; color: #93C5FD; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700;">${p.Ticker}</span></td>
              <td class="num-col">$${p.Revenue_Billions.toFixed(2)}</td>
              <td class="num-col" style="color: ${p.YoY_Growth_Pct > 20 ? '#34D399' : '#93C5FD'}">+${p.YoY_Growth_Pct.toFixed(1)}%</td>
              <td class="num-col">${p.Operating_Margin_Pct.toFixed(1)}%</td>
              <td class="num-col">$${p.Net_Income_Billions.toFixed(2)}</td>
              <td class="num-col">$${p.Free_Cash_Flow_Billions.toFixed(2)}</td>
              <td class="num-col">${p.PE_Ratio.toFixed(1)}x</td>
              <td class="num-col">$${p.Market_Cap_Billions.toFixed(1)}</td>
            </tr>
          `;
        });
      } catch (e) {
        console.error('Failed to load data:', e);
      }
    }

    async function loadReport() {
      try {
        const res = await fetch('/api/report/markdown');
        const md = await res.text();
        
        // Basic Markdown parser for quick rendering
        let html = md
          .replace(/^# (.*$)/gim, '<h1>$1</h1>')
          .replace(/^## (.*$)/gim, '<h2>$1</h2>')
          .replace(/^### (.*$)/gim, '<h3>$1</h3>')
          .replace(/^\\*\\*(.*?)\\*\\*/gim, '<b>$1</b>')
          .replace(/^\\*(.*?)\\*/gim, '<i>$1</i>')
          .replace(/^\\- (.*$)/gim, '<li>$1</li>')
          .replace(/\\n\\n/gim, '<p></p>')
          .replace(/---/gim, '<hr>');

        document.getElementById('reportContent').innerHTML = html;
      } catch (e) {
        document.getElementById('reportContent').innerHTML = '<p>No report loaded.</p>';
      }
    }

    async function loadBenchmarks() {
      try {
        const res = await fetch('/api/benchmarks');
        const b = await res.json();
        document.getElementById('jsonPreview').innerText = JSON.stringify(b, null, 2);

        const routingBody = document.getElementById('routingBody');
        routingBody.innerHTML = '';
        if (b.routing_history) {
          b.routing_history.forEach(item => {
            routingBody.innerHTML += `
              <tr>
                <td><b>#${item.step}</b></td>
                <td><span style="color: #38BDF8; font-weight: 600;">${item.agent_role}</span></td>
                <td>${item.task_name}</td>
                <td class="num-col">${item.duration_seconds?.toFixed(4)}s</td>
                <td><span style="color: #34D399; font-weight: 700;">${item.status}</span></td>
              </tr>
            `;
          });
        }
      } catch (e) {
        console.error('Failed to load benchmarks:', e);
      }
    }

    async function triggerWorkflow() {
      const q = document.getElementById('queryInput').value.trim();
      if (!q) return;

      const btn = document.getElementById('runBtn');
      const progress = document.getElementById('pipelineProgress');
      btn.disabled = true;
      document.getElementById('runBtnText').innerText = 'Multi-Agent Team Working...';
      progress.style.display = 'block';

      // Animate progress steps
      const steps = [
        document.getElementById('step-1'),
        document.getElementById('step-2'),
        document.getElementById('step-3'),
        document.getElementById('step-4'),
        document.getElementById('step-5')
      ];

      let currentStep = 0;
      const interval = setInterval(() => {
        if (currentStep < steps.length - 1) {
          steps[currentStep].classList.remove('active');
          steps[currentStep].classList.add('done');
          currentStep++;
          steps[currentStep].classList.add('active');
        }
      }, 500);

      try {
        const res = await fetch('/api/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: q })
        });
        const result = await res.json();
        
        clearInterval(interval);
        steps.forEach(s => { s.classList.remove('active'); s.classList.add('done'); });

        await loadReport();
        await loadBenchmarks();
        await loadData();
        
        // Refresh PDF iframe
        const frame = document.querySelector('iframe.pdf-frame');
        if (frame) {
          frame.src = '/api/report/pdf?t=' + Date.now();
        }

        alert(`Marketverse Multi-Agent Workflow Completed Successfully!\\nTotal execution time: ${result.duration_seconds}s`);
      } catch (err) {
        alert('Workflow execution error: ' + err);
      } finally {
        btn.disabled = false;
        document.getElementById('runBtnText').innerText = 'Run Multi-Agent Research';
        setTimeout(() => {
          progress.style.display = 'none';
          steps.forEach(s => { s.classList.remove('done', 'active'); });
          steps[0].classList.add('active');
        }, 3000);
      }
    }

    // Initial load
    window.addEventListener('DOMContentLoaded', () => {
      loadData();
      loadReport();
      loadBenchmarks();
    });
  </script>
</body>
</html>
"""


async def homepage(request: Request) -> HTMLResponse:
    """Serve the single-page Marketverse responsive web application."""
    return HTMLResponse(HTML_DASHBOARD)


routes = [
    Route("/", homepage),
    Route("/api/status", api_status),
    Route("/api/run", api_run, methods=["POST"]),
    Route("/api/report/markdown", api_report_markdown),
    Route("/api/report/pdf", api_report_pdf),
    Route("/api/benchmarks", api_benchmarks),
    Route("/api/data", api_data),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"\n[Marketverse] Starting Web Server on http://localhost:{port} ...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

