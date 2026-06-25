from sample_app.agents.planner import PlanStep, QueryPlanner
from sample_app.agents.tools import ToolRegistry
from sample_app.domain.errors import RateLimitExceeded
from sample_app.observability.metrics import Metrics
from sample_app.utils.retry import retry


class AgentExecutor:
    """Executes multi-step plans with retry and rate-limit handling."""

    def __init__(self, planner: QueryPlanner, registry: ToolRegistry, metrics: Metrics):
        self.planner = planner
        self.registry = registry
        self.metrics = metrics

    def run(self, question: str) -> list[str]:
        steps = self.planner.plan(question)
        results = []
        for step in steps:
            results.append(self._execute_step_with_metrics(step))
        return results

    def _execute_step_with_metrics(self, step: PlanStep) -> str:
        self.metrics.increment("agent.step.started")
        try:
            result = self._execute_step_with_retry(step)
        except RateLimitExceeded:
            self.metrics.increment("agent.step.rate_limited")
            raise
        except Exception:
            self.metrics.increment("agent.step.failed")
            raise
        else:
            self.metrics.increment("agent.step.succeeded")
            return result

    @retry(attempts=3, retry_on=(RateLimitExceeded,))
    def _execute_step_with_retry(self, step: PlanStep) -> str:
        tool = self.registry.get(step.tool_name)
        return tool.handler(step.input_text)

