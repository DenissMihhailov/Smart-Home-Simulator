from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_status(self) -> str:
        pass