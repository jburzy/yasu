class Workflow():
    """
    The class representation of the workflow.
    """

    def __init__(self, dag) -> None:

        self._dag = dag
        pass

    def execute(self, backend) -> None:
        pass