from collections import deque

from sample_app.workers.jobs import Job


class JobScheduler:
    def __init__(self):
        self._queue: deque[Job] = deque()
        self._dead_letters: list[Job] = []

    def enqueue(self, job: Job) -> None:
        self._queue.append(job)

    def next_job(self) -> Job | None:
        return self._queue.popleft() if self._queue else None

    def move_to_dead_letter_queue(self, job: Job) -> None:
        self._dead_letters.append(job)

