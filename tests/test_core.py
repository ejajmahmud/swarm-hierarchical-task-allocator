"""Tests for Task Allocator."""
import unittest
from swarm_hierarchical_task_allocator.core import TaskAllocator, AgentProfile, TaskItem

class TestTaskAllocator(unittest.TestCase):
    def test_allocation_and_concurrency(self):
        alloc = TaskAllocator()
        alloc.register_agent(AgentProfile("a1", ["nlp"], max_concurrency=1))
        
        t1 = TaskItem("t1", "nlp")
        t2 = TaskItem("t2", "nlp")
        
        r1 = alloc.allocate(t1)
        self.assertIsNotNone(r1)
        self.assertEqual(r1.agent_id, "a1")
        
        # Concurrency limit reached
        r2 = alloc.allocate(t2)
        self.assertIsNone(r2)
        
        # Release and reallocate
        alloc.release_task("t1")
        r3 = alloc.allocate(t2)
        self.assertIsNotNone(r3)
        self.assertEqual(r3.agent_id, "a1")
