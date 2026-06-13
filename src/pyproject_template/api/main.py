import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from pyproject_template.arithmetic import add_numbers

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

logging.basicConfig(level=logging.INFO)


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def get_root():
    logging.info("Root endpoint accessed")
    return {"msg": "Hello World"}


@app.get("/items/{item_id}")
def get_items(item_id: int, q: str | None = None):
    logging.info(f"Item requested: {item_id}, query: {q}")
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def put_item(item_id: int, item: Item):
    logging.info(f"Item updated: {item_id}, item: {item}")
    return {"item_name": item.name, "item_id": item_id}


@app.get("/numbers/addition/{n1}/{n2}")
def put_numbers_addition(n1: int, n2: int):
    logging.info(f"Adding numbers: {n1} + {n2}")
    return add_numbers(n1, n2)


@app.get("/test")
def get_test():
    logging.info("Test endpoint accessed")
    for i in range(10):
        print(f"testing {i}")
        yield i
