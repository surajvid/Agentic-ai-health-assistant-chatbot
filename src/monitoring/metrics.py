import time
from dataclasses import dataclass, asdict


@dataclass
class QueryMetrics:
    user_query: str
    route: str | None
    safety_triggered: bool
    success: bool
    duration_seconds: float
    error_message: str | None = None

    def to_dict(self):
        return asdict(self)


class Timer:
    """
    Simple timer utility for measuring execution time.
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def duration(self) -> float:
        if self.start_time is None or self.end_time is None:
            return 0.0
        return round(self.end_time - self.start_time, 4)