# core/base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def run(self, contract_code):
        """Each agent must implement this method."""
        pass
