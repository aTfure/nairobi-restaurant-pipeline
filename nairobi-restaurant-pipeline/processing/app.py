from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="nairobi-processing")


class AnalyzeRequest(BaseModel):
    image_url: str


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/analyze")
def analyze(payload: AnalyzeRequest) -> dict[str, object]:
    print("Running Inference...")
    return {
        "food_detected": True,
        "text_extracted": "Sample Menu Item",
    }
