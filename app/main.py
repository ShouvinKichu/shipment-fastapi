from fastapi import FastAPI,HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference

from app.schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from app.database import Database

app = FastAPI()

db = Database()

@app.get("/shipment/latest", response_model=ShipmentRead)
def get_latest_shipment():
    shipment = db.get_latest()
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shipments found!"
        )
    return shipment

@app.get("/shipment/", response_model=ShipmentRead)
def get_shipment(id: int | None = None):
    if id is None:
        shipment = db.get_latest()
    else:
        shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given ID does not exist!"
        )
    return shipment


@app.post("/shipment")
def submit_shipment(shipment : ShipmentCreate) -> dict[str, Any]:
    new_id = db.create(shipment)
    return {"id" : new_id}

@app.put("/shipment", response_model=ShipmentRead)
def shipment_update(id: int, shipment: ShipmentUpdate):
    updated = db.update(id, shipment)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given ID does not exist!"
        )
    return updated


@app.patch("/shipment", response_model=ShipmentRead)
def shipment_patch(id: int, body: ShipmentUpdate):
    updated = db.update(id, body)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given ID does not exist!"
        )
    return updated

@app.delete("/shipment")
def shipment_delete(id: int) -> dict[str, str]:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="shipment not found"
        )
    db.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}

@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="shipment not found"
        )
    return shipment.get(field)


@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "Scalar API",
    )