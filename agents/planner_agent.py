import math
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from typing import Any, Dict, List

from services.session_service import SessionService
from services.memory_service import MemoryService
from services.logging_service import LoggingService
from tools.calculator_tool import CalculatorTool


SYLLABUS_FILE = "syllabus.json"
STUDY_PLAN_FILE = "study_plan.json"


@dataclass
class StudyTask:
    subject: str
    topic: str
    date: str  # ISO string
    planned_minutes: int
    status: str = "planned"  # planned / done / skipped


class PlannerAgent:
    def __init__(
        self,
        session: SessionService,
        memory: MemoryService,
        logger: LoggingService,
        calculator: CalculatorTool,
    ) -> None:
        self.session = session
        self.memory = memory
        self.logger = logger
        self.calculator = calculator

    def _load_syllabus(self) -> Dict[str, Any] | None:
        syllabus = self.memory.load_json(SYLLABUS_FILE)
        if not syllabus:
            self.logger.log("PlannerAgent", "No syllabus found in data/syllabus.json")
            return None
        return syllabus

    def generate_plan(self, num_days: int = 14) -> List[StudyTask]:
        profile = self.session.get("user_profile")
        if not profile:
            self.logger.log(
                "PlannerAgent",
                "No user profile in session. Please run profile intake first.",
            )
            return []

        syllabus = self._load_syllabus()
        if not syllabus:
            return []

        daily_minutes = profile.get("daily_study_minutes", 60)
        start_date = date.today()

        # Flatten all topics
        topics: List[Dict[str, Any]] = []
        for subject in syllabus.get("subjects", []):
            for topic in subject.get("topics", []):
                topics.append(
                    {
                        "subject": subject["name"],
                        "title": topic["title"],
                        "difficulty": topic.get("difficulty", 3),
                    }
                )

        # Estimate minutes for each topic
        topic_durations = [
            self.calculator.estimate_task_duration(t["difficulty"]) for t in topics
        ]
        total_minutes = sum(topic_durations)
        self.logger.log(
            "PlannerAgent",
            "Total estimated study minutes for syllabus.",
            {"total_minutes": total_minutes, "num_topics": len(topics)},
        )

        # Distribute over days
        per_day = self.calculator.distribute_minutes(
            total_minutes, num_days
        )  # total-by-day
        self.logger.log(
            "PlannerAgent",
            "Minutes per day distribution computed.",
            {"per_day": per_day},
        )

        tasks: List[StudyTask] = []
        topic_index = 0
        remaining_for_topic = topic_durations[topic_index] if topics else 0

        for day_index in range(num_days):
            current_date = start_date + timedelta(days=day_index)
            available = min(per_day[day_index], daily_minutes)

            while available > 0 and topic_index < len(topics):
                # Allocate min(remaining_for_topic, available)
                allocated = min(remaining_for_topic, available)
                task = StudyTask(
                    subject=topics[topic_index]["subject"],
                    topic=topics[topic_index]["title"],
                    date=current_date.isoformat(),
                    planned_minutes=allocated,
                )
                tasks.append(task)
                available -= allocated
                remaining_for_topic -= allocated

                if remaining_for_topic <= 0:
                    topic_index += 1
                    if topic_index < len(topics):
                        remaining_for_topic = topic_durations[topic_index]

        # Save plan as JSON
        plan_dicts = [asdict(t) for t in tasks]
        self.memory.save_json(STUDY_PLAN_FILE, {"tasks": plan_dicts})
        self.session.set("study_plan", plan_dicts)
        self.logger.log("PlannerAgent", "Study plan generated and saved.", {"tasks": len(plan_dicts)})

        return tasks

    def get_plan_for_date(self, target_date: date) -> List[StudyTask]:
        plan_data = self.memory.load_json(STUDY_PLAN_FILE)
        if not plan_data:
            return []
        tasks = [
            StudyTask(**t)
            for t in plan_data.get("tasks", [])
            if t["date"] == target_date.isoformat()
        ]
        return tasks

    def update_task_status(self, date_str: str, topic: str, status: str) -> None:
        plan_data = self.memory.load_json(STUDY_PLAN_FILE) or {"tasks": []}
        updated = False
        for t in plan_data["tasks"]:
            if t["date"] == date_str and t["topic"] == topic:
                t["status"] = status
                updated = True
                break
        if updated:
            self.memory.save_json(STUDY_PLAN_FILE, plan_data)
            self.logger.log(
                "PlannerAgent",
                "Updated task status.",
                {"date": date_str, "topic": topic, "status": status},
            )
