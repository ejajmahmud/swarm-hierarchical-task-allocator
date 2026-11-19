"""Core Hierarchical Task Allocator."""
from typing import Dict, List, Optional, Any, Tuple

class AgentProfile:
    def __init__(self, agent_id: str, capabilities: List[str], max_concurrency: int = 4, latency_weight: float = 1.0):
        self.agent_id = agent_id
        self.capabilities = set(capabilities)
        self.max_concurrency = max_concurrency
        self.active_tasks = 0
        self.latency_weight = latency_weight

    def can_handle(self, required_capability: str) -> bool:
        return required_capability in self.capabilities and self.active_tasks < self.max_concurrency

class TaskItem:
    def __init__(self, task_id: str, required_capability: str, priority: int = 1, payload: Optional[Dict[str, Any]] = None):
        self.task_id = task_id
        self.required_capability = required_capability
        self.priority = priority
        self.payload = payload or {}

class BidResult:
    def __init__(self, task_id: str, agent_id: str, score: float, cost: float):
        self.task_id = task_id
        self.agent_id = agent_id
        self.score = score
        self.cost = cost

class TaskAllocator:
    def __init__(self):
        self.agents: Dict[str, AgentProfile] = {}
        self.assignments: Dict[str, str] = {}

    def register_agent(self, profile: AgentProfile):
        self.agents[profile.agent_id] = profile

    def allocate(self, task: TaskItem) -> Optional[BidResult]:
        eligible = [
            a for a in self.agents.values() 
            if a.can_handle(task.required_capability)
        ]
        if not eligible:
            return None

        # Score agents based on load and latency weight (lower load + lower latency = higher score)
        scored = []
        for a in eligible:
            load_factor = (a.active_tasks + 1) / a.max_concurrency
            score = (1.0 / load_factor) / a.latency_weight * (task.priority * 1.0)
            scored.append((score, a))

        scored.sort(key=lambda x: x[0], reverse=True)
        winner_score, winner = scored[0]

        # VCG second-price principle for cost calculation
        second_score = scored[1][0] if len(scored) > 1 else winner_score * 0.8
        payment = second_score

        winner.active_tasks += 1
        self.assignments[task.task_id] = winner.agent_id
        return BidResult(task.task_id, winner.agent_id, winner_score, payment)

    def release_task(self, task_id: str):
        if task_id in self.assignments:
            agent_id = self.assignments.pop(task_id)
            if agent_id in self.agents:
                self.agents[agent_id].active_tasks = max(0, self.agents[agent_id].active_tasks - 1)
