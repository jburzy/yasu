class Backend():
    """
    Base class for the scheduler
    """

    def __init__(self) -> None:
        pass

class SLURMBackend(Backend):

    def __init__(self) -> None:
        super().__init__()

class CondorBackend(Backend):

    def __init__(self) -> None:
        super().__init__()