from collections import Counter
from datetime import date
from typing import Dict, Any

from services.memory_service import MemoryService
from services.logging_service import LoggingService

STUDY_PLAN_FILE = "study_plan.json"


class EvaluationAgent:
    def __init__(self, memory: MemoryService, logger: LoggingService) -> None:
        self.memory = memory
        self.logger = logger

    def evaluate_week(self) -> Dict[str, Any]:
        plan_data = self.memory.load_json(STUDY_PLAN_FILE) or {"tasks": []}
        tasks = plan_data["tasks"]

        if not tasks:
            self.logger.log("EvaluationAgent", "No tasks to evaluate.")
            return {}

        # Filter tasks for last 7 days
        today = date.today()
        recent_tasks = [
            t
            for t in tasks
            if (today - date.fromisoformat(t["date"])).days <= 7
        ]

        total = len(recent_tasks)
        done = sum(1 for t in recent_tasks if t["status"] == "done")
        skipped = sum(1 for t in recent_tasks if t["status"] == "skipped")

        subject_counts = Counter(t["subject"] for t in recent_tasks)
        subject_done = Counter(
            t["subject"] for t in recent_tasks if t["status"] == "done"
        )

        completion_rate = (done / total * 100) if total > 0 else 0

        summary = {
            "total_tasks": total,
            "done": done,
            "skipped": skipped,
            "completion_rate": completion_rate,
            "subject_counts": dict(subject_counts),
            "subject_done": dict(subject_done),
        }

        self.logger.log("EvaluationAgent", "Weekly evaluation summary.", summary)
        return summary

    def print_summary(self) -> None:
        summary = self.evaluate_week()
        if not summary:
            print("\nNo recent tasks to evaluate.")
            return

        print("\nWeekly Progress Summary:")
        print(f"Total tasks: {summary['total_tasks']}")
        print(f"Completed: {summary['done']}")
        print(f"Skipped: {summary['skipped']}")
        print(f"Completion rate: {summary['completion_rate']:.1f}%")

        print("\nTasks per subject:")
        for subj, count in summary["subject_counts"].items():
            done = summary["subject_done"].get(subj, 0)
            print(f"- {subj}: {done}/{count} completed")
