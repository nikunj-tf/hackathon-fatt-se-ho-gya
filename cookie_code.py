import random
import string
import streamlit as st
import requests
import json
import time

def random_str():
    return ''.join(random.choices(string.ascii_lowercase, k=10))

cookie_manager = stx.CookieManager(key="c0")
# cookie_manager2 = stx.CookieManager(key="c1")
st.subheader("All Cookies:")
cookies = cookie_manager.get_all(key='all')
st.write(cookies, key='printAll')

# st.write(cookie_manager.get('application'))

cookieValue = st.text_input("Cookie 1", key="0")
cookieValue2 = st.text_input("Cookie 2", key="1")


st.write(cookieValue, key='printC1')
st.write(cookieValue2, key='printC2')

def setCookieValues(a, b):
    cookie_manager.set('application', a, key="s1")
    cookie_manager.set('application2', b, key="s0")
    try:
        response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": b})
        st.write(json.dumps(response.json()))
        token = response.json().get('token', 'DEFAULT_VALUE')
        print(token)
        st.write(token)
    except Exception as e:
        print(e)
        pdb.post_mortem()

with st.spinner("Setting values"):
    st.button('Try it', on_click=lambda : setCookieValues(cookieValue, cookieValue2))

# sfy.login()
cookie_manager = stx.CookieManager()
old_uuid = cookie_manager.get('uuid')
new_uuid = old_uuid
# st.write(new_uuid)

time.sleep(1)
if not old_uuid:
    new_uuid = random_str()
    print("#####: ", new_uuid)
    cookie_manager.set('uuid', new_uuid, key="unique1")

response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
print(f"######^^^^^^^^^  {response.json()}")
access_token = response.json()['token']
print(f"#####$$$$$$$$$ {access_token}")
print(f"&&&&&&&&&&&& {cookie_manager.get_all(key='all-before')}")
cookie_manager.set('accessToken', 'sdhfghjhasd', key='unique2')
print(f"(((((((((&&&&&&&&&&&& ))))))))){cookie_manager.get_all(key='all-after')}")
    st.write(new_uuid)
    st.write(access_token)

response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
print(f"$$$$$$ {response.json()}")

cookie_manager = stx.CookieManager()
uuid = cookie_manager.get('uuid')
st.write(uuid)

newValue = st.text_input('temp', key="0")
st.button('Try it', on_click=lambda: cookie_manager.set('uuid', newValue))
logging.basicConfig(level=logging.INFO)