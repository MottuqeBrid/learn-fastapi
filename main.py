from fastapi import FastAPI, Path
import json

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data


@app.get("/")
def hello():
    return {"message": "patients management system"}


@app.get("/about")
def about():
    return {"message": "Fully functional API to manage patients records"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def view(
    patient_id: str = Path(
        ..., description="ID of the patient in th Database", example="P001"
    )
):
    # load all the patients data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {"message": "Patient not found"}
