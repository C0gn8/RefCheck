from fastapi import FastAPI
from pydantic import BaseModel

from verifier import verify_reference
from parser import parse_reference

app = FastAPI(title="RefCheck")


class ReferenceRequest(BaseModel):
    reference: str


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "RefCheck"
    }


@app.post("/parse")
def parse(req: ReferenceRequest):
    return parse_reference(req.reference)


@app.post("/verify")
def verify(req: ReferenceRequest):
    return verify_reference(req.reference)
