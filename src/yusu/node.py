import os
from enum import Enum
class TaskStatus(Enum):
    RUNNING = 1
    QUEUED = 2
    COMPLETED = 3
    FAILED = 4

class Node():

    def __init__(self, specs) -> None:

        self.name =  specs.get('name')
        self.payload = specs.get('payload')
        self.cpu_time = specs.get('cpu_time')
        self.memory = specs.get('memory')
        self.dependencies = specs.get('dependencies')

    def execute(self) -> None:

        os.system(self.payload)
        pass

    def query(self) -> TaskStatus:

        return TaskStatus.COMPLETED