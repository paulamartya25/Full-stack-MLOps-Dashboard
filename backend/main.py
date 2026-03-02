from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Factory Dashboard API")

# Configure CORS to allow the frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database models
class Factory(BaseModel):
    total_productive_time: int
    total_production_count: int

class Worker(BaseModel):
    worker_id: int
    active_time: int
    units_produced: int
    utilization: float

class MetricsResponse(BaseModel):
    factory: Factory
    workers: List[Worker]

# Sample data endpoint
@app.get("/metrics/", response_model=MetricsResponse)
async def get_metrics():
    """Return current factory metrics and worker data"""
    factory_data = Factory(
        total_productive_time=3600,
        total_production_count=150
    )
    
    workers_data = [
        Worker(worker_id=1, active_time=2800, units_produced=45, utilization=78),
        Worker(worker_id=2, active_time=3200, units_produced=52, utilization=89),
        Worker(worker_id=3, active_time=2400, units_produced=38, utilization=67),
        Worker(worker_id=4, active_time=3100, units_produced=50, utilization=86),
        Worker(worker_id=5, active_time=1900, units_produced=25, utilization=53),
    ]
    
    return MetricsResponse(factory=factory_data, workers=workers_data)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Serve static frontend files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
