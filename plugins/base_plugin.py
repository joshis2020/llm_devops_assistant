from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def execute(self, prompt: str = None) -> str:
        raise NotImplementedError
