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