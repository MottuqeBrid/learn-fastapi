from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
import json

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data


@app.get("/")
def hello():
    return {"message": "patients management system"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.png")


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn main:app --reload
