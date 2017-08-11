from abc import ABC, abstractmethod

from nodes import *


class Compiler(ABC):
    def __init__(self, tree: CompoundStatement) -> None:
        super().__init__()
        self.tree = tree

    @abstractmethod
    def compile(self):
        raise NotImplementedError

    @abstractmethod
    def build(self, args):
        raise NotImplementedError
