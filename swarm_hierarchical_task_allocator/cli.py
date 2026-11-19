"""CLI for Task Allocator."""
import argparse
from .core import TaskAllocator, AgentProfile, TaskItem

def main():
    parser = argparse.ArgumentParser(description="Swarm Hierarchical Task Allocator CLI")
    parser.add_argument("--demo", action="store_true", help="Run allocator demo")
    args = parser.parse_args()

    alloc = TaskAllocator()
    alloc.register_agent(AgentProfile("coder-1", ["python", "sql"], max_concurrency=2, latency_weight=1.0))
    alloc.register_agent(AgentProfile("researcher-1", ["web_search", "summarize"], max_concurrency=4, latency_weight=1.2))

    t1 = TaskItem("task-1", "python", priority=2)
    res = alloc.allocate(t1)
    if res:
        print(f"Allocated {res.task_id} to {res.agent_id} (Score: {res.score:.2f}, Cost: {res.cost:.2f})")

if __name__ == "__main__":
    main()
