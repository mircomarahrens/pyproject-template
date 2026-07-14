import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from opentelemetry import metrics
from pydantic import BaseModel

from pyproject_template.api.otel import setup_telemetry
from pyproject_template.arithmetic import add_numbers

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Flush/shutdown OpenTelemetry trace and meter providers on shutdown
    if hasattr(app.state, "trace_provider"):
        logging.info("Shutting down telemetry trace provider...")
        app.state.trace_provider.shutdown()
    if hasattr(app.state, "meter_provider"):
        logging.info("Shutting down telemetry meter provider...")
        app.state.meter_provider.shutdown()


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)
setup_telemetry(app)

logging.basicConfig(level=logging.INFO)


meter = metrics.get_meter("fastapi-app-meter")
request_counter = meter.create_counter(
    name="api_requests_total",
    description="Total number of requests to API",
    unit="1",
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def get_root():
    logging.info("Root endpoint accessed")
    request_counter.add(1, {"endpoint": "root"})
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


def get_test():
    for i in range(10):
        print(f"testing {i}")
        yield i


@app.get("/test")
def route_get_test():
    logging.info("Test endpoint accessed")

    def event_generator():
        for i in get_test():
            yield f"{i}\n"

    return StreamingResponse(event_generator(), media_type="text/plain")
