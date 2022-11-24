import subprocess
import os

from enum import Enum
class TaskStatus(Enum):
    RUNNING = 1
    QUEUED = 2
    COMPLETED = 3
    FAILED = 4
    UNDEFINED = 5 
class Backends(Enum):
    LOCAL = 1
    SLURM = 2
class Node():

    def __init__(self, specs) -> None:

        self.name =  specs.get('name')
        self.payload = specs.get('payload')
        self.cpu_time = specs.get('cpu_time')
        self.memory = specs.get('memory')
        self.dependencies = specs.get('dependencies')
        self.backend = Backends.LOCAL
        self.pid = 0
        self.status = TaskStatus.UNDEFINED
        self.process = None

    def execute(self) -> None:

        if not self.payload:
            return

        if self.backend == Backends.LOCAL:
            with open(f"./.__yusu_cache__/{self.name}.log","w") as log:
                payload = f"""if {self.payload}
                then
                    echo "PASS"
                else
                    echo "FAIL"
                fi"""
                self.process = subprocess.Popen(payload,shell=True,stdout=log)
                self.pid = self.process.pid

    def query(self) -> TaskStatus:

        if self.name == "init":
            self.status = TaskStatus.COMPLETED
            return TaskStatus.COMPLETED

        if self.pid == 0:
            self.status = TaskStatus.UNDEFINED
            return TaskStatus.UNDEFINED

        if self.backend == Backends.LOCAL:
            # check if process is still running
            try:
                os.kill(self.pid, 0)
            except OSError:
                return self.get_exit_code()
            else:
                self.status = TaskStatus.RUNNING
                return TaskStatus.RUNNING

        self.status = TaskStatus.COMPLETED
        return TaskStatus.COMPLETED

    def get_exit_code(self) -> TaskStatus:

        with open(f"./.__yusu_cache__/{self.name}.log",'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]

            if "FAIL" in last_line:
                self.status = TaskStatus.FAILED
                return TaskStatus.FAILED
            else:
                self.status = TaskStatus.COMPLETED
                return TaskStatus.COMPLETED
        
