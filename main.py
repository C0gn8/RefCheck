from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="RefCheck")


class ReferenceRequest(BaseModel):
    reference: str


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "RefCheck"
    }


@app.post("/verify")
def verify(req: ReferenceRequest):

    r = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": req.reference,
            "per-page": 1
        }
    )

    data = r.json()

    if not data.get("results"):
        return {
            "status": "not_found"
        }

    result = data["results"][0]

    return {
        "status": "found",
        "title": result.get("display_name"),
        "openalex_id": result.get("id")
    }
