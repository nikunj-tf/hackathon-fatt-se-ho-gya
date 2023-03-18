import os
import time
# from utils import utils
import subprocess
from utils import templates
import streamlit as st
from streamlit_ace import st_ace
import logging
import extra_streamlit_components as stx
import st_redirect as rd
# sfy.login()
from contextlib import contextmanager, redirect_stdout
cookie_manager = stx.CookieManager()
uuid = cookie_manager.get('uuid')
st.write(uuid)

newValue = st.text_input('temp', key="0")
st.button('Try it', on_click=lambda: cookie_manager.set('uuid', newValue))
logging.basicConfig(level=logging.INFO)

my_env = os.environ.copy()
my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

my_env = os.environ.copy()
my_env["TFY_HOST"] = "https://app.devtest.truefoundry.tech/"
my_env["WORKSPACE"] = "tfy-ctl-euwe1-devtest:fat-se-hogya"  # Can be removed if remains unused
WORKSPACE = "tfy-ctl-euwe1-devtest:fat-se-hogya"

def get_template(name):
    if name == "job":
        return templates.job_template
    elif name == "service":
        return templates.service_template
    elif name == "model":
        return templates.model_template
    elif name == "function":
        return templates.function_template
    else:
        return ""


def app():
    st.title("Truefoundry Demo")
    st.subheader("What do you want to deploy?")
    application_options = ["job", "service", "function"]
    application_type = st.selectbox("Select an option", application_options)

    template = get_template(application_type)

    # Display the code editor when a button is clicked
    code = st_ace(language='python', theme='twilight', keybinding='vscode', value=template)
    application_main_path = os.path.join("deploy", application_type, "main.py")
    # if not os.path.exists(application_main_path):
    #     os.
    with open(application_main_path, 'w') as f:
        f.write(code)

    with st.spinner("Running your code locally"):
        print("Running script now")
        with rd.stdout(to=st.text("Code Output:")):
            results = subprocess.run(["python", application_main_path], capture_output=True, text=True)
            print("Results: ", results)

    deploy_button = st.button("Looks great! Let's Deploy.")
    if deploy_button:
        with rd.stdout(to=st.text("Deployment Logs:")):
            proc = subprocess.Popen(["python",f"deploy/{application_type}/deploy.py", "--workspace_fqn", WORKSPACE], env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print("Results: ", proc)

            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                print(line, end='')
if __name__ == '__main__':
    app()