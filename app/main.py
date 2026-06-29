from fastapi import FastAPI,HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference
from app.schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()

shipments = {
    12701: {
        "weight" : 2.1,
        "content" : "Mirror",
        "status" : "Placed"
    },
    12702: {
        "weight" : 7.8,
        "content" : "Books",
        "status" : "in transit"
    },
    12703: {
        "weight" : 1.5,
        "content" : "Smartphone",
        "status" : "delivered"
    },
    12704: {
        "weight" : 12.0,
        "content" : "Garden tools",
        "status" : "pending"
    },
    12705: {
        "weight" : 0.9,
        "content" : "Jewelry",
        "status" : "Placed"
    },
    12706: {
        "weight" : 3.2,
        "content" : "Office chair",
        "status" : "in transit"
    },
    12707: {
        "weight" : 5.4,
        "content" : "Kitchenware",
        "status" : "delivered"
    }
}

@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]

@app.get("/shipment/", response_model=ShipmentRead)
def get_shipment(id : int | None = None):
    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Given ID does not exist!"
        )
    return shipments[id]

@app.post("/shipment")
def submit_shipment(shipment : ShipmentCreate) -> dict[str, Any]:

    new_id = max(shipments.keys()) +1
    shipments[new_id] = {
        "content" : shipment.content,
        "weight" : shipment.weight,
        "status" : "Placed",
    }
    return {"id" : new_id}

@app.put("/shipment", response_model=ShipmentRead)
def shipment_update(id: int, data : ShipmentRead) -> dict[str, Any]:
    shipments[id] = data.model_dump()
    return shipments[id]


@app.patch("/shipment", response_model=ShipmentRead)
def shipment_patch(
    id: int,
    body : ShipmentUpdate
):
    # if content:
    #     shipment["content"] = content
    # if weight:
    #     shipment["weight"] = weight
    # if status:
    #     shipment["status"] = status
    shipments[id].update(body)
    return shipments[id]

@app.delete("/shipment")
def shipment_delete(id : int) -> dict[str,str]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="shipment not found"
        )
    shipments.pop(id)
    return {"detail" : f"Shipment with id #{id} is deleted!"}

@app.get("/shipment/{field}")
def get_shipment_field(field : str, id : int) -> Any:
    return shipments[id][field]


@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "Scalar API",
    )