from collections import deque

class orderQueue:
    def __init__(self):
        self.queue = deque()
        
    def add(self, order):
        self.queue.append(order)
        
    def process_next(self):
        if self.queue:
            return self.queue.popleft()
        return None
    
order_queue = orderQueue()