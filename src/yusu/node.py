class Node():

    def __init__(self, payload, cpu_time, memory, account) -> None:

        self._payload = payload
        self._cpu_time = cpu_time
        self._memory = memory
        self._account = account

    def execute(self) -> None:
        pass