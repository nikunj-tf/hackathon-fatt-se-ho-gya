job_template = {
    "ml" : """
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

X, y = load_iris(as_frame=True, return_X_y=True)
X = X.rename(columns={
        "sepal length (cm)": "sepal_length",
        "sepal width (cm)": "sepal_width",
        "petal length (cm)": "petal_length",
        "petal width (cm)": "petal_width",
})

# NOTE:- You can pass these configurations via command line
# arguments, config file, environment variables.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Initialize the model
clf = LogisticRegression(solver="liblinear")
# Fit the model
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print(classification_report(y_true=y_test, y_pred=preds))
""",

    "hello" : """
print("Hello World")
""",

    "empty": """
""",

}

service_template = {
    "ml" : """
import os
import joblib
import pandas as pd
from fastapi import FastAPI

model = joblib.load('/'.join(os.path.realpath(__file__).split('/')[:-1]) + "/iris_classifier.joblib")

app = FastAPI(root_path=os.getenv("TFY_SERVICE_ROOT_PATH"))

@app.post("/predict")
def predict(
    sepal_length: float, sepal_width: float, petal_length: float, petal_width: float
):
    data = dict(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )
    prediction = int(model.predict(pd.DataFrame([data]))[0])
    return {"prediction": prediction}
""",

    "hello" : """
from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def hello_world():
    return {"message": "Hello World"}
""",

    "empty": """
""",
}

deploy_message = """
To deploy your code, click the button below to go to the Truefoundry website.
"""

saving_code = """
#
# def random_str():
#     return ''.join(random.choices(string.ascii_lowercase, k=10))
#
# cookie_manager = stx.CookieManager(key="c0")
# # cookie_manager2 = stx.CookieManager(key="c1")
# st.subheader("All Cookies:")
# cookies = cookie_manager.get_all(key='all')
# st.write(cookies, key='printAll')
#
# # st.write(cookie_manager.get('application'))
#
# cookieValue = st.text_input("Cookie 1", key="0")
# cookieValue2 = st.text_input("Cookie 2", key="1")
#
#
# st.write(cookieValue, key='printC1')
# st.write(cookieValue2, key='printC2')
#
# def setCookieValues(a, b):
#     cookie_manager.set('application', a, key="s1")
#     cookie_manager.set('application2', b, key="s0")
#     try:
#         response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": b})
#         st.write(json.dumps(response.json()))
#         token = response.json().get('token', 'DEFAULT_VALUE')
#         print(token)
#         st.write(token)
#     except Exception as e:
#         print(e)
#         pdb.post_mortem()

# with st.spinner("Setting values"):
#     st.button('Try it', on_click=lambda : setCookieValues(cookieValue, cookieValue2))

# # sfy.login()
# cookie_manager = stx.CookieManager()
# old_uuid = cookie_manager.get('uuid')
# new_uuid = old_uuid
# # st.write(new_uuid)
#
# time.sleep(1)
# if not old_uuid:
#     new_uuid = random_str()
#     print("#####: ", new_uuid)
#     cookie_manager.set('uuid', new_uuid, key="unique1")
#
# response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
# print(f"######^^^^^^^^^  {response.json()}")
# access_token = response.json()['token']
# print(f"#####$$$$$$$$$ {access_token}")
# print(f"&&&&&&&&&&&& {cookie_manager.get_all(key='all-before')}")
# cookie_manager.set('accessToken', 'sdhfghjhasd', key='unique2')
# print(f"(((((((((&&&&&&&&&&&& ))))))))){cookie_manager.get_all(key='all-after')}")
    # st.write(new_uuid)
    # st.write(access_token)

# response = requests.post(CONTROL_PLANE_URL + '/v1/service-account/anonymous-token', data={"name": new_uuid})
# print(f"$$$$$$ {response.json()}")

"""




