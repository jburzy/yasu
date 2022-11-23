
from .node import Node, TaskStatus
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("output.log"),
        logging.StreamHandler()
    ]
)
class DAG():
    def __init__(self) -> None:
        self._graph = {}
        self._nodes = {}

        self._init = Node({'name': 'init', 'dependencies': [], 'payload': ''})
        self.add_node(self._init)

    def add_node(self, node: Node) -> None:
        self._nodes[node.name] = node
        self._graph[node] = []

        if node.dependencies:
            for parent_name in node.dependencies:
                self._graph[self._nodes[parent_name]].append(node)

    def execute(self) -> None:

        #breadth first search
        visited = []
        queue = [self._init]
        while queue:
            node = queue.pop(0) 
            logging.info(f"Visiting node {node.name}")

            # check the status of the current node
            node_status = node.query()
            logging.info(f"Querying node {node.name} status...{node_status}")

            # check if dependencies have finished before executing
            dependencies_finished = True
            for parent_proc in node.dependencies:
                status = self._nodes[parent_proc].query()
                logging.info(f"Parent node {self._nodes[parent_proc].name} has status {status}")
                if status != TaskStatus.COMPLETED:
                    dependencies_finished = False
                    continue  

            execute_node = dependencies_finished and node_status == TaskStatus.UNDEFINED

            if execute_node:
                logging.info(f"Executing node {node.name}")
                node.execute()
            elif not dependencies_finished:
                logging.info(f"Dependency not complete! Skipping this node.")
            elif node_status == TaskStatus.RUNNING:
                logging.info(f"Node is currently running. Skipping this node.")
            elif node_status == TaskStatus.COMPLETED:
                logging.info(f"Node is finished! Skipping this node.")

            for child_proc in self._graph[self._nodes[node.name]]:
                if child_proc not in visited:
                    visited.append(child_proc)
                    queue.append(child_proc)

    def check_for_cycles(self) -> bool:
        return True
