from datetime import date
from typing import List

from services.session_service import SessionService
from services.logging_service import LoggingService
from agents.planner_agent import PlannerAgent, StudyTask


class CoachAgent:
    """
    Main conversational / guidance agent.
    LLM integration (e.g., Gemini) could be added to enhance responses.
    """

    def __init__(
        self,
        session: SessionService,
        planner: PlannerAgent,
        logger: LoggingService,
    ) -> None:
        self.session = session
        self.planner = planner
        self.logger = logger

    def show_today_plan(self) -> List[StudyTask]:
        today = date.today()
        tasks = self.planner.get_plan_for_date(today)
        self.logger.log("CoachAgent", "Fetched today's plan.", {"count": len(tasks)})
        if not tasks:
            print("No tasks planned for today. You may need to generate a plan.")
            return []
        print(f"\nYour plan for today ({today.isoformat()}):")
        for i, t in enumerate(tasks, start=1):
            print(
                f"{i}. [{t.status}] {t.subject} - {t.topic} "
                f"({t.planned_minutes} min)"
            )
        return tasks

    def mark_task_status(self, tasks: List[StudyTask]) -> None:
        if not tasks:
            return
        choice = input(
            "\nEnter the number of the task you completed or skipped (or press Enter to skip): "
        )
        if not choice.strip():
            return

        idx = int(choice) - 1
        if idx < 0 or idx >= len(tasks):
            print("Invalid choice.")
            return

        status_choice = input("Type 'done' or 'skipped': ").strip().lower()
        if status_choice not in ("done", "skipped"):
            print("Invalid status.")
            return

        task = tasks[idx]
        self.planner.update_task_status(
            date_str=task.date, topic=task.topic, status=status_choice
        )
        print(f"Updated task '{task.topic}' to status '{status_choice}'.")

    def quick_motivation(self) -> None:
        # Simple static responses; could be replaced with LLM.
        messages = [
            "Small steps every day lead to big results.",
            "Consistency beats intensity. Keep going!",
            "You're building a better future for yourself right now.",
        ]
        # pick one deterministically based on date so it feels dynamic
        i = date.today().day % len(messages)
        msg = messages[i]
        self.logger.log("CoachAgent", "Motivational message served.", {"message": msg})
        print(f"\nCoach: {msg}")
