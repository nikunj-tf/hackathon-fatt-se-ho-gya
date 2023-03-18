import argparse
import logging

from servicefoundry.function_service import FunctionService

from inspect import getmembers, isfunction
import main

all_functions = getmembers(main, isfunction)
print(all_functions)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", required=True, type=str)
args = parser.parse_args()

service = FunctionService(name="func-service")
for func in all_functions:
    service.register_function(func[1])

service.deploy(workspace_fqn=args.workspace_fqn)
