
from .node import Node
class DAG():
    def __init__(self) -> None:
        self._graph = {}
        self._nodes = {}

        self._init = Node({'name': 'init', 'dependencies': [], 'payload': ''})
        self.add_node(self._init)

    def add_node(self, node: Node) -> None:
        print(self._graph)
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

            node.execute()
            for child_proc in self._graph[self._nodes[node.name]]:
                if child_proc not in visited:
                    visited.append(child_proc)
                    queue.append(child_proc)

    def check_for_cycles(self) -> bool:
        return True
