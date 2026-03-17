from pydantic import (
    BaseModel,
    EmailStr,
    computed_field,
)
from typing import List, Dict


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float  # weight in kg
    height: float  # height in meters
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("BMI", patient.bmi)
    print("-----------------------------")


patient_info = {
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@gmail.com",
    "weight": 70.5,
    "height": 1.8,
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
    "weight": 60.5,
    "height": 1.8,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {"email": "john.doe@gmail.com", "phone": "123-456-7890"},
    "linkedin": "https://www.linkedin.com/in/johndoe",
}
patient1 = Patient(**patient_info)
patient2 = Patient(**patient_info1)

insert_patient_data(patient1)
insert_patient_data(patient2)
