from fastapi import FastAPI

app = FastAPI(title="RefCheck")

@app.get("/")
def root():
    return {
        "status": "running",
        "project": "RefCheck"
    }
