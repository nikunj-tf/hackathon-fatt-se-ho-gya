import streamlit as st
import os
import time
# from utils import utils
import subprocess
from utils import templates
from streamlit_ace import st_ace
import logging
import servicefoundry as sfy
import extra_streamlit_components as stx
import st_redirect as rd
import random
import string
import requests

my_env = os.environ.copy()
my_env["TFY_HOST"] = "https://app.devtest.truefoundry.tech/"
my_env["WORKSPACE"] = "tfy-ctl-euwe1-devtest:fat-se-hogya"  # Can be removed if remains unused
WORKSPACE = "tfy-ctl-euwe1-devtest:fat-se-hogya"
CONTROL_PLANE_URL = 'https://app.devtest.truefoundry.tech'
def random_str():
     return ''.join(random.choices(string.ascii_lowercase, k=10))

cookie_manager = stx.CookieManager()
old_uuid = cookie_manager.get('uuid')

time.sleep(2)

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
print("BEFORE THE LOOP: ", old_uuid)

if not old_uuid:
    rand_str = random_str()
    cookie_manager.set('uuid', rand_str, key="unique1")
    response = requests.post(CONTROL_PLANE_URL + '/api/svc/v1/service-account/anonymous-token', data={"name": rand_str})
    access_token = response.json()['token']
    print("INSIDE THE CONDITION: ", access_token)
    if st.session_state['access_token'] is None:
        st.session_state['access_token'] = access_token
    print(access_token)

print("OUTSIDE OF LOOP: ", st.session_state['access_token'])

def get_template(application_type, name):
    if application_type == "job":
        return templates.job_template[name]
    elif application_type == "service":
        return templates.service_template[name]
    else:
        return ""

def app():
    st.title("Truefoundry Demo")
    st.subheader("What do you want to deploy?")
    application_options = ["job", "service", "function"]
    application_type = st.selectbox("Select the type of application", application_options)

    template_options = ["hello", "ml", "empty"]
    template_name = st.selectbox("Select the template", template_options)

    template = get_template(application_type, template_name)

    # Display the code editor when a button is clicked
    code = st_ace(
        value=template,
        height=500,
        language="python",
        theme="chrome",
        keybinding="vscode",
        font_size=15,
        show_gutter=False,
        wrap=True,
        auto_update=True
    )

    command = None
    if application_type == "service":
        command = st.text_input(label="Enter the command to run your service locally. Eg. uvicorn ")


    application_main_path = os.path.join("deploy", application_type, "main.py")
    with open(application_main_path, 'w') as f:
        f.write(code)

    if st.button("Run your code locally"):
        print("Running script now")
        if application_type == "job":
            with rd.stdout(to=st.text("Code Output:"), format='code'):
                results = subprocess.run(["python", application_main_path], capture_output=True, text=True)
                print("Results: ", results.stdout, results.stderr)

        if application_type == "service":
            with rd.stdout(to=st.text("Code Output:"), format='code'):
                proc = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                print("Results: ", proc)

                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    print(line, end='')


    deploy_button = st.button("Looks great! Let's Deploy.")
    if deploy_button:
        with rd.stdout(to=st.text("Deployment Logs:"), format='code'):
            proc = subprocess.Popen(["python",f"deploy/{application_type}/deploy.py", "--workspace_fqn", WORKSPACE], env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print("Results: ", proc)

            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                print(line, end='')


if __name__ == '__main__':
    app()
