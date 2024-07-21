from typing import Annotated, Optional
import os

from fastapi import FastAPI, Path, Query, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sqlite3

from model import Model

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_model():
    return Model()


class Item(BaseModel):
    item: str


@app.get("/")
async def get_all_items(model: Model = Depends(get_model)):
    try:
        ret = {}
        for item in model.get_all_items():
            ret[item[0]] = item[1]
        return ret
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/{id}")
async def get_item(
    id: Annotated[int, Path(title="The ID of the item to get")],
    model: Model = Depends(get_model),
):
    try:
        item = model.get_item(id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item": item}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/")
async def create_or_update_item(
    item: Annotated[str, Query(title="The item to create or update")],
    id: Optional[
        Annotated[
            int, Query(title="The ID of the item to update (if exists)", default=None)
        ]
    ] = None,
    model: Model = Depends(get_model),
):
    try:
        if id is not None and model.get_item(id) is not None:
            if not model.update_item(id, item):
                raise HTTPException(status_code=404, detail="Item not found")
            return {"message": "Item updated successfully"}
        else:
            item_id = model.create_item(item)
            return {"item_id": item_id}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.put("/{id}")
async def update_item(
    id: Annotated[int, Path(title="The ID of the item to update")],
    item: Item,
    model: Model = Depends(get_model),
):
    try:
        if not model.update_item(id, item.item):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item updated successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/{id}")
async def delete_item(
    id: Annotated[int, Path(title="The ID of the item to delete")],
    model: Model = Depends(get_model),
):
    try:
        if not model.delete_item(id):
            raise HTTPException(status_code=404, detail="Item not found")
        return Response(status_code=204)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
