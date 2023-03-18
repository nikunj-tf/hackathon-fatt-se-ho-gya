import webbrowser
import signal
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

tfy_api_key = st.session_state['access_token']
if tfy_api_key is not None:
    os.environ["tfy_api_key"] = tfy_api_key
else:
    os.environ["tfy_api_key"] = ' eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxzV0lDNWtkU1V1bXg1ckg5NkR6bFdYUGxJTSJ9.eyJhdWQiOiI4OTUyNTNhZi1lYzlkLTRiZTYtODNkMS02ZjI0OGU2NDRlNzkiLCJleHAiOjM2NzkxMzQ2MzUsImlhdCI6MTY3OTEzNDYzNSwiaXNzIjoidHJ1ZWZvdW5kcnkuY29tIiwic3ViIjoiY2xmZHRlbzNuMDNkYjFoZGlmN3E4MnE2OSIsImp0aSI6ImQ2YmE2NDAwLTFjZmUtNDllOC04NDM2LWU5MjczZmNhOWVhYiIsInVzZXJuYW1lIjoibWF1ZXJodHZxZCIsInVzZXJUeXBlIjoic2VydmljZWFjY291bnQiLCJ0ZW5hbnROYW1lIjoidHJ1ZWZvdW5kcnkiLCJhcHBsaWNhdGlvbklkIjoiODk1MjUzYWYtZWM5ZC00YmU2LTgzZDEtNmYyNDhlNjQ0ZTc5In0.WsTlJbZIte9mEGhI9O8X_MqsXNDiP7qFKzvyj8mfcZeLRodTQZ275yQsq6cc61TVTz95S2_phD7JUVX7AMPZ5duNssix7hZEYVdDMzw7As0BTCzaLB-EYYq-Q-579u1rrMHrAuePlGJ2fRrl8HrW2pvoNh1gaA9qMClfOBRee4OcCbUl9nCWPutihxW6o-VlP2ZW2msOZAwImo7U394cYnNnH24NyZeEQp30ljn1Doyacqt1VMf7XOp9SFJTPr8WeOXwHbw6rnT7DAQJuBqZpYvFWrHmzp8yp5DccyD6f5e4y7p0t7OM59iplSBldFvvQEknqgFayt-Df_DFKxLX_g'

print("ENVIRON: ", os.environ["tfy_api_key"])

if not old_uuid:
    rand_str = random_str()
    cookie_manager.set('uuid', rand_str, key="unique1")
    response = requests.post(CONTROL_PLANE_URL + '/api/svc/v1/service-account/anonymous-token', data={"name": rand_str})
    access_token = response.json()['token']
    # cookie_manager.set('token', access_token, key="unique2")
    print("INSIDE THE CONDITION: ", access_token)
    if st.session_state['access_token'] is None:
        st.session_state['access_token'] = access_token
    print(access_token)

print("OUTSIDE OF LOOP: ", st.session_state['access_token'])

# if st.button("Go to Deployment Dashboard"):
#     # url = endpoint.split('')[1]
#     url = CONTROL_PLANE_URL + f'/loginsuccess?accessToken={st.session_state["access_token"]}&refreshToken=dummy'
#     st.write(f"Here's your magic url: {url}")
#     print(url)
#     webbrowser.open_new_tab(url)


def get_template(application_type, name):
    if application_type == "job":
        return templates.job_template[name]
    elif application_type == "service":
        return templates.service_template[name]
    else:
        return ""

def app():
    proc = None
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
        command = st.text_input(label="Enter the command to run your service locally", value="uvicorn main:app --port 8000 --host 0.0.0.0")
        my_env["command"] = command


    application_main_path = os.path.join("deploy", application_type, "main.py")
    with open(application_main_path, 'w') as f:
        f.write(code)

    if st.button("Run your code locally"):
        print("Running script now")
        if application_type == "job":
            with rd.stdout(to=st.text("Code Output:"), format='code'):
                proc = subprocess.run(["python", application_main_path], capture_output=True, text=True)
                print("Results: ", proc.stdout, proc.stderr)

        if application_type == "service":
            with rd.stdout(to=st.text("Code Output:"), format='code'):
                local_command = command.replace("main", "deploy.service.main")
                proc = subprocess.Popen(local_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                print("Results: ", proc)

                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    print(line, end='')

        # Add "Stop Local Run" button and terminate the subprocess if it's running
        if proc is not None:
            if st.button("Stop Local Run"):
                print("Stopping local run...")
                proc.send_signal(signal.SIGTERM)


    deploy_button = st.button("Looks great! Let's Deploy.")
    if deploy_button:
        with rd.stdout(to=st.text("Deployment Logs:"), format='code'):
            proc = subprocess.Popen(["python", f"deploy/{application_type}/deploy.py", "--workspace_fqn", WORKSPACE], env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print("Results: ", proc)

            endpoint = None
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                print(line, end='')
                if "INFO:servicefoundry:You can find the application on the dashboard:-" in line:
                    endpoint = line.split("INFO:servicefoundry:You can find the application on the dashboard:-")[-1].strip()
                elif "Deployment Failed. Please refer to the logs for additional details - " in line:
                    endpoint = line.split("Deployment Failed. Please refer to the logs for additional details - ")[-1].strip()
            if endpoint:
                st.text(endpoint)
                if st.button("Go to Deployment Dashboard"):
                    # url = endpoint.split('')[1]
                    url = CONTROL_PLANE_URL + f'/loginsuccess?accessToken={st.session_state["access_token"]}&refreshToken=dummy'
                    st.write(f"Here's your magic url: {url}")
                    print(url)
                    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    app()
