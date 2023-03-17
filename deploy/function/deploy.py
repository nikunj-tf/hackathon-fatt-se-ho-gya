import argparse
import logging

from servicefoundry.function_service import FunctionService

from script import normal, uniform

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", required=True, type=str)
args = parser.parse_args()

service = FunctionService(name="func-service")
service.register_function(normal)
service.register_function(uniform)

service.deploy(workspace_fqn=args.workspace_fqn)