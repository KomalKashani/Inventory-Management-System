from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Increment


# Firebase init
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI(title="Electronics Inventory API")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model
class Item(BaseModel):
    name: str
    count: int

# Add item
@app.post("/items")
def add_item(item: Item):
    doc_ref = db.collection("items").add(item.dict())
    return {"id": doc_ref[1].id}

# Get all items
@app.get("/items")
def get_items():
    items = []
    for doc in db.collection("items").stream():
        data = doc.to_dict()
        data["id"] = doc.id
        items.append(data)
    return items

# Update item
@app.put("/items/{name}")
def update_item(name: str, item: Item):
    doc = db.collection("items").document(name)
    if not doc.get().exists:
        raise HTTPException(status_code=404, detail="Item not found")
    doc.set(item.dict())
    return {"message": "Item updated"}

@app.patch("/items/{item_id}/increase")
def increase_count(item_id: str):
    doc = db.collection("items").document(item_id)
    if not doc.get().exists:
        raise HTTPException(status_code=404, detail="Item not found")
    doc.update({"count": Increment(1)})


@app.patch("/items/{name}/decrease")
def decrease_count(name: str):
    doc = db.collection("items").document(name)
    snap = doc.get()
    if not snap.exists:
        raise HTTPException(status_code=404, detail="Item not found")

    if snap.to_dict()["count"] <= 0:
        raise HTTPException(status_code=400, detail="Count already zero")

    doc.update({"count": Increment(-1)})
    return {"message": "Count decreased"}

# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    db.collection("items").document(item_id).delete()
    return {"message": "Item deleted"}

