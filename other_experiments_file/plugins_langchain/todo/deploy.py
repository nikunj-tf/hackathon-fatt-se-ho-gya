import argparse
import logging
from servicefoundry import Build, PythonBuild, Service, Resources, Port

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", required=True, type=str)
args = parser.parse_args()

image = Build(
      build_spec=PythonBuild(
        command="python todo_api.py",
        requirements_path="requirements.txt",
      )
)
  
service = Service(
    name="todo-trial",
    image=image,
    ports=[
      Port(
        port=5002,
        host="trial-todo-api.tfy-ctl-euwe1-devtest.devtest.truefoundry.tech"
      )
    ],
    env={
      "UVICORN_WEB_CONCURRENCY": "1",
      "ENVIRONMENT": "dev"
    }
)

service.deploy(workspace_fqn=args.workspace_fqn)
