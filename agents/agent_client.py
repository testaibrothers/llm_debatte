from abc import ABC, abstractmethod

class AgentClient(ABC):
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config

    @abstractmethod
    def call(self, prompt: str) -> str:
        pass
