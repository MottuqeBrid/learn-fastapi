from pydantic import (
    BaseModel,
    EmailStr,
    model_validator,
)
from typing import List, Dict


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact:
            raise ValueError("Patient above 60 must have an emergency contact")


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)


patient_info = {
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@gmail.com",
    "weight": 70.5,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {
        "email": "john.doe@gmail.com",
        "phone": "123-456-7890",
        "emergency": "+1234567890",
    },
    "linkedin": "https://www.linkedin.com/in/johndoe",
}
patient_info1 = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@gmail.com",
    "weight": 70.5,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {"email": "john.doe@gmail.com", "phone": "123-456-7890"},
    "linkedin": "https://www.linkedin.com/in/johndoe",
}
patient1 = Patient(**patient_info)
patient2 = Patient(**patient_info1)

insert_patient_data(patient1)
insert_patient_data(patient2)
