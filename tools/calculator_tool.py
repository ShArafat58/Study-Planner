from typing import List


class CalculatorTool:
    """
    Simple helper for time calculations.
    """

    @staticmethod
    def estimate_task_duration(difficulty: int) -> int:
        """
        Rough estimate in minutes based on a difficulty level (1-5).
        """
        base = 25
        return base + (difficulty - 1) * 10

    @staticmethod
    def distribute_minutes(total_minutes: int, num_days: int) -> List[int]:
        """
        Evenly distribute total minutes across a number of days.
        """
        base = total_minutes // num_days
        remainder = total_minutes % num_days
        distribution = [base] * num_days
        for i in range(remainder):
            distribution[i] += 1
        return distribution
