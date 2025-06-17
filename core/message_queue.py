# core/message_queue.py

from collections import deque

class MessageQueue:
    def __init__(self):
        self.queue = deque()

    def send(self, message):
        self.queue.append(message)

    def receive(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0
