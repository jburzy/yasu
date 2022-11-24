import argparse
from .utils import build_dag_from_yaml
from .dag import DAG
from .workflow import Workflow
import sys
import os
import hashlib
import dill
import logging
import shutil

def cache_file(input_file):

    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(input_file, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input yaml file with the workflow specification')
    parser.add_argument('-b', '--backend', choices=['slurm','condor'], default = 'slurm', help = 'Backend to use')
    parser.add_argument('--clear_cache', action='store_true', help = 'Remove the cache before running')
    parser.add_argument('d', '--debug', action='store_true', help = 'Set logging level to debug')
    args = parser.parse_args()


    logging.basicConfig(
        level=logging.INFO if not args.debug else logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("output.log"),
            logging.StreamHandler()
        ]
    )

    if args.clear_cache:
        logging.info("Clearing cache directory as requested...")
        shutil.rmtree("./.__yusu_cache__") 

    file_cache = cache_file(args.input_file)

    history = {}
    if not os.path.isdir("./.__yusu_cache__"):
        os.mkdir("./.__yusu_cache__")
    try:
        cache = open('./.__yusu_cache__/cache.pickle', 'rb+')
        history = dill.load(cache)
    except IOError:
        logging.info("Cache file not found. Creating file .__yusu_cache__/cache.pickle.")
        cache = open('./.__yusu_cache__/cache.pickle', 'wb')

    if file_cache in history:
        logging.info(f"File {args.input_file} found in cache, executing cached workflow.")
        workflow = history[file_cache]
        workflow.execute()
    else:
        logging.info(f"File {args.input_file} not found in cache, building new workflow.")
        dag = build_dag_from_yaml(args.input_file)
        workflow = Workflow(dag)
        workflow.execute()

        history[file_cache] = workflow
        dill.dump(history, cache)

if __name__=="__main__":
    main()