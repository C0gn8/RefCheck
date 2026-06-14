from fastapi import FastAPI
from pydantic import BaseModel

from verifier import verify_reference
from parser import parse_reference
from bibliography_parser import split_references
from audit import generate_audit

app = FastAPI(title="RefCheck")


class ReferenceRequest(BaseModel):
    reference: str


class BatchReferenceRequest(BaseModel):
    references: list[str]


class BibliographyRequest(BaseModel):
    text: str


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

    for reference in req.references:

        results.append({
            "reference": reference,
            "result": verify_reference(reference)
        })

    return generate_audit(results)


@app.post("/verify_text")
def verify_text(req: BibliographyRequest):

    references = split_references(req.text)

    results = []

    for reference in references:

        results.append({
            "reference": reference,
            "result": verify_reference(reference)
        })

    return {
        "references": results,
        "audit": generate_audit(results)
    }


@app.post("/audit")
def audit(req: BibliographyRequest):

    references = split_references(req.text)

    results = []

    for reference in references:

        results.append({
            "reference": reference,
            "result": verify_reference(reference)
        })

    return generate_audit(results)
