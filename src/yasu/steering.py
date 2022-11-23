import argparse
from .utils import build_dag_from_yaml
from .dag import DAG
from .workflow import Workflow

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input yaml file with the workflow specification')
    parser.add_argument('-b', '--backend', choices=['slurm','condor'], default = 'slurm', help = 'Backend to use')
    args = parser.parse_args()

    dag = build_dag_from_yaml(args.input_file)
    workflow = Workflow(dag)
    workflow.execute(args.backend)

if __name__=="__main__":
    main()