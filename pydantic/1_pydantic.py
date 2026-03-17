from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

import pydantic

print(pydantic.__version__)


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Give the name of the patient in less then 50 characters",
            examples=["Sahoreia", "Mottuqe"],
        ),
    ]
    email: EmailStr
    age: int = Field(gt=0)
    weight: Annotated[
        float, Field(gt=0, strict=True, description="Weight of the patient in kg")
    ]
    married: Annotated[
        bool, Field(default=None, description="Is the patient married or not")
    ]
    allergies: Annotated[Optional[List[str]], Field(max_length=5, default=None)]
    contact: Dict[str, str]
    linkedin: AnyUrl


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print(patient.linkedin)


patient_info = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "weight": 70.5,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {"email": "john.doe@example.com", "phone": "123-456-7890"},
    "linkedin": "https://www.linkedin.com/in/johndoe",
}
patient_info1 = {
    "name": "John Doe",
    "age": "30",
    "email": "john.doe@example.com",
    "weight": 70.5,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {"email": "john.doe@example.com", "phone": "123-456-7890"},
    "linkedin": "https://www.linkedin.com/in/johndoe",
}
patient1 = Patient(**patient_info)
patient2 = Patient(**patient_info1)

insert_patient_data(patient1)
insert_patient_data(patient2)
