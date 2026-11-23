"""Tests verifying CrewAI hierarchical orchestration, agent roles, and benchmarking logs."""

import os
import json
import pytest
from pathlib import Path
from crewai import Process

from crew.crew import MarketverseCrew
from crew.utils.benchmark import BenchmarkTracker


def test_agent_roles_and_goals():
    """Verify that the Crew contains the exact required agent roles and goals."""
    crew_orchestrator = MarketverseCrew(query="Test Query")
    
    # 1. Lead Researcher Agent
    assert crew_orchestrator.researcher.role == "Market Research Specialist"
    assert "Query search search networks" in crew_orchestrator.researcher.goal

    # 2. Data Analyst Agent
    assert crew_orchestrator.analyst.role == "Financial Data Analyst"
    assert "Parse data matrices using Pandas" in crew_orchestrator.analyst.goal

    # 3. Content Writer Agent
    assert crew_orchestrator.writer.role == "Technical Reports Writer"
    assert "Synthesize information, write sections, and structure copy" in crew_orchestrator.writer.goal

    # 4. Hierarchical Process
    assert crew_orchestrator.crew.process == Process.hierarchical


def test_benchmark_tracker_lifecycle(tmp_path: Path):
    """Verify start_task, complete_task, timing calculation, and JSON persistence."""
    tracker = BenchmarkTracker(query="Benchmarking Test")
    
    t_id = tracker.start_task(
        task_name="Unit Test Task",
        agent_role="Test Agent",
        delegated_by="Manager LLM"
    )
    assert t_id in tracker.active_tasks

    completed = tracker.complete_task(t_id, status="COMPLETED", output_preview="Sample preview")
    assert completed["status"] == "COMPLETED"
    assert "duration_seconds" in completed
    assert completed["duration_seconds"] >= 0.0

    target_json = tmp_path / "benchmarks_test.json"
    saved_path = tracker.save(str(target_json))
    assert os.path.exists(saved_path)

    with open(saved_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["query"] == "Benchmarking Test"
    assert data["status"] == "SUCCESS"
    assert len(data["routing_history"]) == 1
    assert "Test Agent" in data["agent_benchmarks"]


def test_marketverse_crew_kickoff(tmp_path: Path, mock_csv_file: Path):
    """Verify end-to-end kickoff creates outputs, tracks benchmarks, and synthesizes report."""
    crew_orchestrator = MarketverseCrew(
        query="Mock Sector Evaluation",
        csv_path=str(mock_csv_file)
    )
    result = crew_orchestrator.kickoff()

    assert "markdown_report" in result
    assert "benchmarks" in result
    assert len(result["benchmarks"]["routing_history"]) == 3
    assert result["benchmarks"]["status"] == "SUCCESS"
