"""Execution Benchmarking & Analytics Tracker for Marketverse.

Captures, traces, and persists execution metrics to benchmarks.json.
Logs duration for each agent task and traces dynamic task routing history.
"""

import os
import json
import time
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class BenchmarkTracker:
    """Tracks execution performance and task routing history across hierarchical agents."""

    def __init__(self, query: str = "Market Analysis", workflow_id: Optional[str] = None):
        self.workflow_id = workflow_id or f"wf_{int(time.time())}"
        self.query = query
        self.start_wall_time = time.time()
        self.start_iso = datetime.now().isoformat()
        self.end_wall_time: Optional[float] = None
        self.end_iso: Optional[str] = None
        self.routing_history: List[Dict[str, Any]] = []
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.step_counter = 0

    def start_task(
        self,
        task_name: str,
        agent_role: str,
        delegated_by: str = "Manager LLM",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Mark the start of an agent task."""
        self.step_counter += 1
        task_id = f"task_{self.step_counter}_{agent_role.lower().replace(' ', '_')}"
        start_time = time.time()
        
        task_record = {
            "step": self.step_counter,
            "task_id": task_id,
            "task_name": task_name,
            "agent_role": agent_role,
            "delegated_by": delegated_by,
            "start_time": datetime.now().isoformat(),
            "_start_timestamp": start_time,
            "status": "IN_PROGRESS",
            "metadata": metadata or {}
        }
        self.active_tasks[task_id] = task_record
        return task_id

    def complete_task(
        self,
        task_id: str,
        status: str = "COMPLETED",
        output_preview: Optional[str] = None,
        extra_metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Record completion of an agent task and compute elapsed time."""
        if task_id not in self.active_tasks:
            raise KeyError(f"Task ID '{task_id}' was not started.")

        task_record = self.active_tasks.pop(task_id)
        end_time = time.time()
        duration = round(end_time - task_record["_start_timestamp"], 4)
        
        task_record["end_time"] = datetime.now().isoformat()
        task_record["duration_seconds"] = duration
        task_record["status"] = status
        del task_record["_start_timestamp"]

        if output_preview:
            task_record["output_preview"] = output_preview[:200]
        if extra_metrics:
            task_record.update(extra_metrics)

        self.routing_history.append(task_record)
        return task_record

    def finalize(self, status: str = "SUCCESS") -> Dict[str, Any]:
        """Finalize the workflow run and assemble benchmark metrics."""
        self.end_wall_time = time.time()
        self.end_iso = datetime.now().isoformat()
        total_duration = round(self.end_wall_time - self.start_wall_time, 4)

        # Summarize by agent
        agent_benchmarks: Dict[str, Dict[str, Any]] = {}
        for entry in self.routing_history:
            role = entry["agent_role"]
            if role not in agent_benchmarks:
                agent_benchmarks[role] = {
                    "task_count": 0,
                    "total_duration_seconds": 0.0,
                    "status": "COMPLETED"
                }
            agent_benchmarks[role]["task_count"] += 1
            agent_benchmarks[role]["total_duration_seconds"] = round(
                agent_benchmarks[role]["total_duration_seconds"] + entry.get("duration_seconds", 0.0), 4
            )

        benchmark_report = {
            "workflow_id": self.workflow_id,
            "query": self.query,
            "status": status,
            "start_time": self.start_iso,
            "end_time": self.end_iso,
            "total_duration_seconds": total_duration,
            "task_count": len(self.routing_history),
            "routing_history": self.routing_history,
            "agent_benchmarks": agent_benchmarks,
            "system_environment": {
                "python_version": platform.python_version(),
                "os": platform.system(),
                "os_release": platform.release(),
                "processor": platform.processor() or "x86_64"
            }
        }
        return benchmark_report

    def save(self, filepath: str = "benchmarks.json") -> Path:
        """Save the benchmark report to disk as JSON."""
        target = Path(filepath)
        target.parent.mkdir(parents=True, exist_ok=True)
        report = self.finalize()
        
        with open(target, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return target
