from .dag import DAG
from .node import Node
import yaml

def build_dag_from_yaml(input_file: str) -> DAG:
    '''
    parses the input YAML file and builds the dag

            Args:
                    files: 

            Returns:
                    DAG
    '''

    workflow_specs = {}
    with open(input_file) as f:
        try:
            workflow_specs = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    dag = DAG()
    for step in workflow_specs['stages']:
        node = Node(step)
        dag.add_node(node)

    return dag