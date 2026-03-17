from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address


def insert_patient_data(patient: Patient):

    print("-----------------------------")


address_dect = {"city": "New York", "state": "NY", "pin": "10001"}

address1 = Address(**address_dect)
patient_dect = {"name": "John Doe", "gender": "Male", "age": 30, "address": address1}

patient1 = Patient(**patient_dect)


print(patient1)
print(patient1.name)
print(patient1.address.city)
