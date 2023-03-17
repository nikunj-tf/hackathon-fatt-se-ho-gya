
import os
import enum
from pathlib import Path

import subprocess
import streamlit as st
from streamlit_ace import st_ace
import logging
from servicefoundry import Job, Build, PythonBuild, Resources, Param
import extra_streamlit_components as stx
import servicefoundry as sfy
import st_redirect as rd
# sfy.login()
from contextlib import contextmanager, redirect_stdout
cookie_manager = stx.CookieManager()
uuid = cookie_manager.get('uuid')
st.write(uuid)

newValue = st.text_input('temp', key="0")
st.button('Try it', on_click=lambda : cookie_manager.set('uuid', newValue))
logging.basicConfig(level=logging.INFO)

WORKSPACE = 'demo-euwe1-production:aviso-ci-cd'

deployment_type = st.sidebar.radio("What do you want to deploy", ('Function', 'Service', 'Job'))
job_template = """
import time

def print_count():
    for i in range(5):
        print(f"Printing index {i}")
        time.sleep(0.1)
print_count()
"""

if deployment_type == 'Function':

    st.subheader("Use this template or add your own code to editor")
    # st.code(job_template)
    content = st_ace(language='python', theme='twilight', keybinding='vscode', value=job_template)
    print(content)
    with open("script.py", 'w') as f:
        f.write(content)
    with st.spinner("Running your code locally"):
        print("Running script now")
        result = subprocess.run(["python", "script.py"], capture_output=True, text=True)
        print("Results: ", result)
        st.text_area("Code Output", result.stdout + result.stderr)

    deploy_button = st.button("Looks great! Let's Deploy.")
    if deploy_button:
        with st.spinner("Deploying your code"):
            to_out = st.empty()
            solver_output_filepath = f"{Path.cwd()}/data/solver_out.txt"
            # with rd.stdout(to=to_out, to_file=solver_output_filepath, format="text", max_buffer=10000):
            image = Build(
                build_spec=PythonBuild(
                    command="python script.py"
                )
            )
            job = Job(
                name="test-script",
                image=image,
            )
            deploy_out = job.deploy(workspace_fqn=WORKSPACE)
            print("###########: ", deploy_out)
            print("World")


elif deployment_type == 'Service':
    print("Service")
elif deployment_type == 'Job':
    print("Job")

# Spawn a new ace editor

