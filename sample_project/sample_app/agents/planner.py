from dataclasses import dataclass


@dataclass
class PlanStep:
    tool_name: str
    input_text: str


class QueryPlanner:
    def plan(self, question: str) -> list[PlanStep]:
        steps = [PlanStep("search", question)]
        if "compare" in question.lower():
            steps.append(PlanStep("summarize", "compare retrieved evidence"))
        if "error" in question.lower():
            steps.append(PlanStep("diagnose", "inspect error messages and stack traces"))
        return steps

