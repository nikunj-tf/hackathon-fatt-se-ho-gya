import argparse
import logging
from servicefoundry import Build, Job, PythonBuild, Resources

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", required=True, type=str)
args = parser.parse_args()

# First we define how to build our code into a Docker image
image = Build(
    build_spec=PythonBuild(
        command="python main.py",
        requirements_path="requirements.txt",
    )
)
job = Job(
    name="iris-train-job",
    image=image,
    resources=Resources(memory_limit=1500, memory_request=100),
    env={
      "TFY_API_KEY": tfy_api_key
    }
)
job.deploy(workspace_fqn=args.workspace_fqn)
