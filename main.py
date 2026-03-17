from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[
        str, Field(..., description="Name of the patient", examples=["John Doe"])
    ]
    city: Annotated[
        str,
        Field(..., description="City of the patient is living", examples=["New York"]),
    ]
    age: Annotated[
        int, Field(..., gt=0, lt=120, description="Age of the patient", examples=[20])
    ]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient", examples=["male"]),
    ]
    height: Annotated[
        float,
        Field(
            ..., description="Height of the patient in meters", gt=0, examples=[1.75]
        ),
    ]
    weight: Annotated[
        float,
        Field(
            ..., description="Weight of the patient in kilograms", gt=0, examples=[70.0]
        ),
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(default=None, description="Name of the patient", examples=["John Doe"]),
    ]
    city: Annotated[
        Optional[str],
        Field(
            default=None,
            description="City of the patient is living",
            examples=["New York"],
        ),
    ]
    age: Annotated[
        Optional[int],
        Field(
            default=None, gt=0, lt=120, description="Age of the patient", examples=[20]
        ),
    ]
    gender: Annotated[
        Optional[Literal["male", "female", "others"]],
        Field(
            default=None,
            description="Gender of the patient",
            examples=["male"],
        ),
    ]
    height: Annotated[
        Optional[float],
        Field(
            default=None,
            description="Height of the patient in meters",
            gt=0,
            examples=[1.75],
        ),
    ]
    weight: Annotated[
        Optional[float],
        Field(
            default=None,
            description="Weight of the patient in kilograms",
            gt=0,
            examples=[70.0],
        ),
    ]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "patients management system"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.png")


@app.get("/about")
def about():
    return FileResponse("files/demo.html", status_code=200)


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
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"),
    order: str = Query("asc", description="Sorting order: asc or desc"),
):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by value. Must be one of {valid_fields}",
        )
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Must be 'asc' or 'desc'",
        )
    data = load_data()
    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == "desc")
    )
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    # load existing data
    data = load_data()
    # check if patient with the same ID already exists
    if patient.id in data:
        raise HTTPException(
            status_code=400, detail="Patient with this ID already exists"
        )
    # add new patient to the data
    data[patient.id] = patient.model_dump(exclude=["id"])
    # save the updated data back to the file
    save_data(data)
    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully", "patient_id": patient.id},
    )


@app.put("/edit/{patient_id}")
def update_patient(
    patient_update: PatientUpdate,
    patient_id: str = Path(
        ..., description="ID of the patient in th Database", example="P001"
    ),
):
    print(patient_id, patient_update)
    # load existing data
    data = load_data()
    # check if patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404, detail=f"Patient with ID {patient_id} not found"
        )
    # update patient data
    existing_patient_info = data[patient_id]
    # update patient data with the new values from patient_update
    patient_update_dict = patient_update.model_dump(exclude_unset=True)
    for key, value in patient_update_dict.items():
        existing_patient_info[key] = value
    # save the updated data back to the file
    existing_patient_info["id"] = patient_id
    patient_pydentic = Patient(**existing_patient_info)
    patient_pydentic_obj = patient_pydentic.model_dump(exclude=["id"])
    data[patient_id] = patient_pydentic_obj
    save_data(data)
    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully", "patient_id": patient_id},
    )


@app.delete("/delete/{patient_id}")
def delete_patient(
    patient_id: str = Path(
        ..., description="ID of the patient in th Database", example="P001"
    )
):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=404, detail=f"Patient with ID {patient_id} not found"
        )
    del data[patient_id]
    save_data(data)
    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully", "patient_id": patient_id},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn main:app --reload
