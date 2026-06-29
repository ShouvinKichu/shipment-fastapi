from fastapi import FastAPI,HTTPException, status
from typing import Any
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {
        "weight" : 2.1,
        "content" : "Mirror",
        "status" : "shipped"
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
        "status" : "shipped"
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

@app.get("/shipment/")
def get_shipment(id : int | None = None) -> dict[str,Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Given ID does not exist!"
        )
    return shipments[id]

@app.post("/shipment")
def submit_shipment(data : dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weight = data["weight"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Max weight is 25 kg"
        )

    new_id = max(shipments.keys()) +1
    shipments[new_id] = {
        "content" : content,
        "weight" : weight,
        "status" : "placed",
    }
    return {"id" : new_id}

@app.get("/shipment/{field}")
def get_shipment_field(field : str, id : int) -> Any:
    return shipments[id][field]


@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "Scalar API",
    )