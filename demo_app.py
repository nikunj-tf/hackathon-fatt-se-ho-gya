import os
import time
import subprocess
from utils import templates
import streamlit as st
from streamlit_ace import st_ace
import logging
import requests
import extra_streamlit_components as stx
import st_redirect as rd
import json
import random
import string

HOST_NAME = "sath-me-smart.demo.truefoundry.com"
CONTROL_PLANE_URL = "https://app.devtest.truefoundry.tech/api/svc"

def random_str():
    return ''.join(random.choices(string.ascii_lowercase, k=10))


# sfy.login()
cookie_manager = stx.CookieManager()
old_uuid = cookie_manager.get('uuid')
new_uuid = old_uuid
# st.write(new_uuid)

time.sleep(1)
if not old_uuid:
    new_uuid = random_str()
    # print("#####: ", new_uuid)
    cookie_manager.set('uuid', new_uuid, key="uuid")
    response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
    # print(f"######^^^^^^^^^  {response.json()}")

    access_token = response.json()['token']
    # print(f"#####$$$$$$$$$ {access_token}")
    cookie_manager.set('accessToken', access_token, key='accessToken')
    # st.write(new_uuid)
    # st.write(access_token)

# response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
# print(f"$$$$$$ {response.json()}")

WORKSPACE = 'demo-euwe1-production:aviso-ci-cd'

my_env = os.environ.copy()
my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

my_env = os.environ.copy()
my_env["TFY_HOST"] = "https://app.devtest.truefoundry.tech/"
my_env["WORKSPACE"] = "tfy-ctl-euwe1-devtest:fat-se-hogya"  # Can be removed if remains unused


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
    st.title("TrueFoundry Demo")
    st.subheader("What do you want to deploy?")
    application_options = ["job", "service", "function"]
    application_type = st.selectbox("Select an option", application_options)

    template = get_template(application_type)

    # Display the code editor when a button is clicked
    code = st_ace(language='python', theme='twilight', keybinding='vscode', value=template)
    application_main_path = os.path.join("deploy", application_type, "main.py")

    with open(application_main_path, 'w') as f:
        f.write(code)

    with st.spinner("Running your code locally"):
        print("Running script now")
        result = subprocess.run(["python", application_main_path], capture_output=True, text=True)
        print("Results: ", result)
        st.text_area("Code Output", result.stdout + result.stderr)

    deploy_button = st.button("Looks great! Let's Deploy.")
    if deploy_button:
        with st.spinner("Deploying your code"):
            with rd.stdout, rd.stderr(format='markdown'):
                subprocess.run(["python", f"deploy/{application_type}/deploy.py", "--workspace_fqn", WORKSPACE])
                time.sleep(200)
                st.text("Python deployed")


if __name__ == '__main__':
    app()
