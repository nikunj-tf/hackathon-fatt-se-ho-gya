import logging

from servicefoundry import Build, PythonBuild, Service, Resources

logging.basicConfig(level=logging.INFO)
WORKSPACE = 'tfy-ctl-euwe1-devtest:fat-se-hogya'

image=Build(
    build_spec=PythonBuild(
      command="streamlit run demo_app.py",
      requirements_path="requirements.txt",
    )
)
service = Service(
  name="streamlitdeployquick",
  image=image,
  ports=[{"port": 8501, "host": "app-fatt-se-ho-gya.tfy-ctl-euwe1-devtest.devtest.truefoundry.tech"}],
  resources=Resources(memory_limit=1500, memory_request=1000),
)
service.deploy(workspace_fqn=WORKSPACE)
