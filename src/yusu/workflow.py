from .node import Node
class Workflow():
    """
    The class representation of the workflow.
    """

    def __init__(self, dag) -> None:

        self._dag = dag
        pass

    def execute(self) -> None:

        self._dag.execute()
