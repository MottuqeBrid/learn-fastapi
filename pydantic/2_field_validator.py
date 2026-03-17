from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
        # Extract the domain from the email
        domain_name = value.split("@")[1]
        if domain_name not in valid_domains:
            raise ValueError(f"Invalid email domain. Must be one of {valid_domains}")
        return value

    @field_validator("name", mode="after")
    @classmethod
    def name_validator(cls, value):
        return value.upper()


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
    "age": 30,
    "email": "john.doe@gmail.com",
    "weight": 70.5,
    "married": "True",
    "allergies": ["peanuts", "pollen", "dust"],
    "contact": {"email": "john.doe@gmail.com", "phone": "123-456-7890"},
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
