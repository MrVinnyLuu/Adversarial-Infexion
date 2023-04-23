from heapq import heappush, heappop
import random

# PriorityQueue implemented using heapq
# The closer the priority value is to 0, the higher its priority (ignoring negative numbers)
# Each item is a tuple of (priority, value)
class PQNode:

    def __init__(self, value, priority=0):
        self.value = value
        self.priority = priority
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        else:
            return random.choice([True, False])

class PriorityQueue:

    def __init__(self):
        self.heap = []
    
    def add(self, node: PQNode):
        heappush(self.heap, node)
    
    def pop(self):
        return None if not self.heap else heappop(self.heap).value