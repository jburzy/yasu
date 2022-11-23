from .dag import DAG
#import yaml

def build_dag_from_yaml(input_file) -> DAG:
    '''
    parses the input YAML file and builds the dag

            Args:
                    files: 

            Returns:
                    DAG
    '''

    try:
        with open(input_file) as f:
            pass
    except FileNotFoundError:
        print(f"File {input_file} does not exist!")

    return DAG()