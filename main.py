from services.session_service import SessionService
from services.memory_service import MemoryService
from services.logging_service import LoggingService
from tools.calculator_tool import CalculatorTool

from agents.profile_agent import ProfileAgent
from agents.planner_agent import PlannerAgent
from agents.coach_agent import CoachAgent
from agents.evaluation_agent import EvaluationAgent


def main() -> None:
    session = SessionService()
    memory = MemoryService(base_dir="data")
    logger = LoggingService()
    calculator = CalculatorTool()

    profile_agent = ProfileAgent(session, memory, logger)
    planner_agent = PlannerAgent(session, memory, logger, calculator)
    coach_agent = CoachAgent(session, planner_agent, logger)
    eval_agent = EvaluationAgent(memory, logger)

    # Try to load existing profile into session
    existing_profile = profile_agent.load_profile()
    if existing_profile:
        session.set("user_profile", existing_profile.__dict__)

    while True:
        print(
            "\n=== EduGuide: Study Planner ===\n"
            "1. Set up / update my profile\n"
            "2. Generate study plan\n"
            "3. Show today's plan\n"
            "4. Mark a task as done or skipped\n"
            "5. Show weekly summary\n"
            "0. Exit\n"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            profile_agent.interactive_intake()

        elif choice == "2":
            days_str = input(
                "For how many days should I generate a plan? (default 14): "
            ).strip()
            num_days = int(days_str) if days_str else 14
            planner_agent.generate_plan(num_days=num_days)
            print(f"Study plan generated for {num_days} days.")

        elif choice == "3":
            tasks = coach_agent.show_today_plan()
            coach_agent.quick_motivation()

        elif choice == "4":
            tasks = coach_agent.show_today_plan()
            coach_agent.mark_task_status(tasks)

        elif choice == "5":
            eval_agent.print_summary()

        elif choice == "0":
            print("Goodbye! Keep studying consistently 😊")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
