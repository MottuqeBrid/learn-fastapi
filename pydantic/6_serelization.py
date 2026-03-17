from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str = "Male"
    age: int
    address: Address


def insert_patient_data(patient: Patient):

    print("-----------------------------")


address_dect = {"city": "New York", "state": "NY", "pin": "10001"}

address1 = Address(**address_dect)
patient_dect = {"name": "John Doe", "age": 30, "address": address1}

patient1 = Patient(**patient_dect)

temp = patient1.model_dump(
    exclude_unset=True
)  # exclude_unset=True will exclude the default values from the output
print(temp)
print(type(temp))
temp2 = patient1.model_dump_json()
print(temp2)
print(type(temp2))
