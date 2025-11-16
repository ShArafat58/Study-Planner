from dataclasses import dataclass, asdict
from typing import List

from services.session_service import SessionService
from services.memory_service import MemoryService
from services.logging_service import LoggingService


USER_PROFILE_FILE = "user_profile.json"


@dataclass
class UserProfile:
    name: str
    grade: str
    subjects: List[str]
    daily_study_minutes: int
    preference: str  # e.g. "morning" or "evening"


class ProfileAgent:
    def __init__(
        self,
        session: SessionService,
        memory: MemoryService,
        logger: LoggingService,
    ) -> None:
        self.session = session
        self.memory = memory
        self.logger = logger

    def interactive_intake(self) -> UserProfile:
        self.logger.log("ProfileAgent", "Starting interactive intake.")

        name = input("What is your name? ")
        grade = input("What grade or level are you in? ")
        subjects_raw = input("Enter your subjects (comma separated): ")
        subjects = [s.strip() for s in subjects_raw.split(",") if s.strip()]
        daily_minutes_str = input("How many minutes per day can you study? ")
        preference = input("Do you prefer studying in the morning or evening? ")

        daily_study_minutes = int(daily_minutes_str)

        profile = UserProfile(
            name=name,
            grade=grade,
            subjects=subjects,
            daily_study_minutes=daily_study_minutes,
            preference=preference,
        )

        # store in session & memory
        self.session.set("user_profile", asdict(profile))
        self.memory.save_json(USER_PROFILE_FILE, asdict(profile))
        self.logger.log("ProfileAgent", "User profile saved.", asdict(profile))

        return profile

    def load_profile(self) -> UserProfile | None:
        data = self.memory.load_json(USER_PROFILE_FILE)
        if not data:
            self.logger.log("ProfileAgent", "No existing profile found.")
            return None
        self.logger.log("ProfileAgent", "Loaded existing profile.", data)
        return UserProfile(**data)
