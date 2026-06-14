from fastapi import FastAPI
from pydantic import BaseModel

from verifier import verify_reference
from parser import parse_reference

app = FastAPI(title="RefCheck")


class ReferenceRequest(BaseModel):
    reference: str


class BatchReferenceRequest(BaseModel):
    references: list[str]


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


@app.post("/verify_batch")
def verify_batch(req: BatchReferenceRequest):

    results = []

    verified = 0
    possible = 0
    weak = 0
    not_found = 0

    for reference in req.references:

        result = verify_reference(reference)

        results.append(result)

        if result["status"] == "verified":
            verified += 1

        elif result["status"] == "possible_match":
            possible += 1

        elif result["status"] == "weak_match":
            weak += 1

        elif result["status"] == "not_found":
            not_found += 1

    return {
        "total": len(req.references),
        "verified": verified,
        "possible_matches": possible,
        "weak_matches": weak,
        "not_found": not_found,
        "results": results
    }
