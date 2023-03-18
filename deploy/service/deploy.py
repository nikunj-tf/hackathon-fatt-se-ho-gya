from ...demo_app import command
import argparse
import logging
from servicefoundry import Build, PythonBuild, Service, Resources

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", required=True, type=str)
args = parser.parse_args()

image = Build(
      build_spec=PythonBuild(
        command=command,
        requirements_path="requirements.txt",
      )
)
  
service = Service(
    name="fastapi",
    image=image,
    ports=[{"port": 8000, "host": "fatt-se-ho-gya.tfy-ctl-euwe1-devtest.devtest.truefoundry.tech"}],
    resources=Resources(
      cpu_request=0.5,
      cpu_limit=1,
      memory_request=1000,
      memory_limit=1500
    ),
)
service.deploy(workspace_fqn=args.workspace_fqn)
