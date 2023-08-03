from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@app.get("/")
def index() -> Dict[str, Dict[int, Item]]:
    return {"items": items}