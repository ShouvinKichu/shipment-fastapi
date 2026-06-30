from random import randint
from pydantic import BaseModel, Field
from enum import Enum

class ShipmentStatus(str, Enum):
    placed = "Placed"
    in_transit = "In Transit"
    out_of_delivery = "Out for delivery"
    delivered = "Delivered"


def random_destination():
    return randint(11000,19999)

class BaseShipment(BaseModel):
    content : str = Field(description="Contents to be shipped", max_length=20)
    weight : float = Field(description="Weight is in Kg", lt=25)
    destination : int | None = Field(description="Destination Zipcode", default_factory=random_destination)


class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class Order(BaseModel):
        price : int
        title : str
        description : str

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status : ShipmentStatus