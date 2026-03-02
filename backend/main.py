from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from datetime import datetime
from collections import defaultdict
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Factory Dashboard API")

# Configure CORS to allow the frontend to communicate
# Support both local development and Render deployment
allowed_origins = [
    "http://localhost:5173",      # Local development
    "http://localhost:3000",      # Alternative local port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# Add Render production URLs if they exist in environment
import os
if os.getenv("RENDER") == "true":
    # On Render, allow requests from the production frontend domain
    allowed_origins.extend([
        "https://*.onrender.com",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATABASE SETUP ====================

# Create database - Support both SQLite and PostgreSQL
# Default to SQLite locally, but allow DATABASE_URL env var for production
database_url = os.getenv("DATABASE_URL", "sqlite:///./factory_dashboard.db")

# For PostgreSQL, ensure we're using the right driver
if database_url.startswith("postgresql://"):
    # Replace old postgres:// with postgresql:// if needed
    database_url = database_url.replace("postgres://", "postgresql://")

# Different connection args for different databases
if "postgresql" in database_url:
    engine = create_engine(database_url, echo=False)
else:
    # SQLite setup
    engine = create_engine(database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== DATABASE MODELS ====================

class WorkerModel(Base):
    """Database model for workers"""
    __tablename__ = "workers"
    
    worker_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    shift = Column(String, default="Morning")
    active_time = Column(Integer, default=0)  # in seconds
    idle_time = Column(Integer, default=0)    # in seconds
    units_produced = Column(Integer, default=0)
    utilization = Column(Float, default=0.0)

class WorkstationModel(Base):
    """Database model for workstations"""
    __tablename__ = "workstations"
    
    station_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, default="general")
    occupancy_time = Column(Integer, default=0)  # in seconds
    utilization = Column(Float, default=0.0)
    units_produced = Column(Integer, default=0)
    throughput_rate = Column(Float, default=0.0)  # units per hour

class AIEventModel(Base):
    """Database model for AI events"""
    __tablename__ = "ai_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    worker_id = Column(Integer, nullable=False)
    station_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)  # working, idle, absent, product_count
    confidence = Column(Float, default=0.95)
    count = Column(Integer, default=0)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkerEventModel(Base):
    """Database model for legacy worker events"""
    __tablename__ = "worker_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    duration = Column(Integer, default=0)
    notes = Column(String, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)

# ==================== PYDANTIC MODELS (API REQUEST/RESPONSE) ====================

class Factory(BaseModel):
    total_productive_time: int
    total_production_count: int
    average_production_rate: float
    average_utilization: float

class Worker(BaseModel):
    worker_id: int
    name: str
    active_time: int
    idle_time: int
    units_produced: int
    utilization: float

class Workstation(BaseModel):
    station_id: int
    name: str
    occupancy_time: int
    utilization: float
    units_produced: int
    throughput_rate: float

class MetricsResponse(BaseModel):
    factory: Factory
    workers: List[Worker]
    workstations: List[Workstation]

class AIEvent(BaseModel):
    timestamp: str
    worker_id: int
    station_id: int
    event_type: str  # working, idle, absent, product_count
    confidence: float = 0.95
    count: int = 0
    notes: str = ""

class EventResponse(BaseModel):
    success: bool
    message: str

class WorkerEvent(BaseModel):
    worker_id: int
    event_type: str  # e.g., "break", "task_start", "task_end", "error"
    duration: int = 0  # in seconds
    notes: str = ""

# ==================== SAMPLE DATA & DATABASE INITIALIZATION ====================

SAMPLE_WORKERS = [
    {"worker_id": 1, "name": "Alice Johnson", "shift": "Morning", "active_time": 2800, "idle_time": 600, "units_produced": 45, "utilization": 78},
    {"worker_id": 2, "name": "Bob Smith", "shift": "Morning", "active_time": 3200, "idle_time": 400, "units_produced": 52, "utilization": 89},
    {"worker_id": 3, "name": "Carlos Martinez", "shift": "Afternoon", "active_time": 2400, "idle_time": 800, "units_produced": 38, "utilization": 67},
    {"worker_id": 4, "name": "Diana Lee", "shift": "Afternoon", "active_time": 3100, "idle_time": 500, "units_produced": 50, "utilization": 86},
    {"worker_id": 5, "name": "Ethan Brown", "shift": "Night", "active_time": 1900, "idle_time": 1100, "units_produced": 25, "utilization": 53},
    {"worker_id": 6, "name": "Fiona Garcia", "shift": "Night", "active_time": 2500, "idle_time": 700, "units_produced": 48, "utilization": 77},
]

SAMPLE_WORKSTATIONS = [
    {"station_id": 1, "name": "Assembly Line A", "type": "assembly", "occupancy_time": 3400, "utilization": 80, "units_produced": 95, "throughput_rate": 13.8},
    {"station_id": 2, "name": "Assembly Line B", "type": "assembly", "occupancy_time": 3600, "utilization": 85, "units_produced": 108, "throughput_rate": 15.1},
    {"station_id": 3, "name": "Quality Check", "type": "qc", "occupancy_time": 2800, "utilization": 78, "units_produced": 45, "throughput_rate": 16.4},
    {"station_id": 4, "name": "Packaging", "type": "packaging", "occupancy_time": 3200, "utilization": 82, "units_produced": 88, "throughput_rate": 17.7},
    {"station_id": 5, "name": "Testing Station", "type": "testing", "occupancy_time": 2400, "utilization": 71, "units_produced": 62, "throughput_rate": 19.0},
    {"station_id": 6, "name": "Finishing", "type": "finishing", "occupancy_time": 3100, "utilization": 79, "units_produced": 98, "throughput_rate": 20.3},
]

def init_db():
    """Initialize database with sample data"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_workers = db.query(WorkerModel).count()
        if existing_workers == 0:
            logger.info("🗄️ Initializing database with sample data...")
            # Add workers
            for worker in SAMPLE_WORKERS:
                db.add(WorkerModel(**worker))
            # Add workstations
            for station in SAMPLE_WORKSTATIONS:
                db.add(WorkstationModel(**station))
            db.commit()
            logger.info("✅ Database initialized successfully")
    finally:
        db.close()

def reset_sample_data():
    """Reset all data to sample state"""
    db = SessionLocal()
    try:
        logger.info("🔄 Resetting database to sample data...")
        # Clear all tables
        db.query(AIEventModel).delete()
        db.query(WorkerEventModel).delete()
        db.query(WorkerModel).delete()
        db.query(WorkstationModel).delete()
        db.commit()
        
        # Re-populate with sample data
        for worker in SAMPLE_WORKERS:
            db.add(WorkerModel(**worker))
        for station in SAMPLE_WORKSTATIONS:
            db.add(WorkstationModel(**station))
        db.commit()
        logger.info("✅ Database reset successfully")
    finally:
        db.close()

# ==================== UTILITY FUNCTIONS ====================

def calculate_hash(timestamp: str, worker_id: int, station_id: int, event_type: str) -> str:
    """Calculate a hash for duplicate detection"""
    return f"{worker_id}_{station_id}_{timestamp}_{event_type}"

def is_duplicate(db: Session, timestamp: str, worker_id: int, station_id: int, event_type: str) -> bool:
    """Check if event is a duplicate in database"""
    existing = db.query(AIEventModel).filter(
        AIEventModel.timestamp == timestamp,
        AIEventModel.worker_id == worker_id,
        AIEventModel.station_id == station_id,
        AIEventModel.event_type == event_type
    ).first()
    return existing is not None

def handle_out_of_order(db: Session, event: AIEventModel):
    """Handle out-of-order events by ensuring they're stored in chronological order"""
    db.add(event)
    db.commit()

def calculate_ai_event_metrics(db: Session):
    """Calculate metrics from AI events in database"""
    worker_active = defaultdict(int)
    worker_idle = defaultdict(int)
    worker_units = defaultdict(int)
    station_occupancy = defaultdict(int)
    station_units = defaultdict(int)
    
    # Get all events from database
    ai_events = db.query(AIEventModel).all()
    
    for event in ai_events:
        if event.event_type == "working":
            worker_active[event.worker_id] += 300  # 5 minutes per event
            station_occupancy[event.station_id] += 300
        elif event.event_type == "idle":
            worker_idle[event.worker_id] += 300
        elif event.event_type == "product_count":
            worker_units[event.worker_id] += event.count
            station_units[event.station_id] += event.count
    
    # Map to store initial sample values
    initial_worker_units = {w["worker_id"]: w["units_produced"] for w in SAMPLE_WORKERS}
    initial_station_units = {s["station_id"]: s["units_produced"] for s in SAMPLE_WORKSTATIONS}
    
    # Update worker metrics in database
    for worker_id in range(1, 7):
        worker = db.query(WorkerModel).filter(WorkerModel.worker_id == worker_id).first()
        if worker:
            if worker_active[worker_id] > 0:
                worker.active_time = worker_active[worker_id]
            if worker_idle[worker_id] > 0:
                worker.idle_time = worker_idle[worker_id]
            # Set units_produced to initial value + calculated events
            worker.units_produced = initial_worker_units.get(worker_id, 0) + worker_units[worker_id]
            
            total_time = worker.active_time + worker.idle_time
            if total_time > 0:
                worker.utilization = int((worker.active_time / total_time) * 100)
    
    # Update workstation metrics in database
    for station_id in range(1, 7):
        station = db.query(WorkstationModel).filter(WorkstationModel.station_id == station_id).first()
        if station:
            if station_occupancy[station_id] > 0:
                station.occupancy_time = station_occupancy[station_id]
            # Set units_produced to initial value + calculated events
            station.units_produced = initial_station_units.get(station_id, 0) + station_units[station_id]
    
    db.commit()
    
    db.commit()


# ==================== API ENDPOINTS ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/metrics", response_model=MetricsResponse)
@app.get("/metrics/", response_model=MetricsResponse)
async def get_metrics(db: Session = Depends(get_db)):
    """Return current factory metrics and worker data"""
    workers = db.query(WorkerModel).all()
    workstations = db.query(WorkstationModel).all()
    
    total_productive = sum(w.active_time for w in workers)
    total_produced = sum(w.units_produced for w in workers)
    avg_utilization = sum(w.utilization for w in workers) / len(workers) if workers else 0
    avg_production_rate = total_produced / 6 if total_produced > 0 else 0
    
    factory_data = Factory(
        total_productive_time=total_productive,
        total_production_count=total_produced,
        average_production_rate=round(avg_production_rate, 2),
        average_utilization=round(avg_utilization, 1)
    )
    
    workers_list = [
        Worker(
            worker_id=w.worker_id,
            name=w.name,
            active_time=w.active_time,
            idle_time=w.idle_time,
            units_produced=w.units_produced,
            utilization=float(w.utilization)
        )
        for w in workers
    ]
    
    workstations_list = [
        Workstation(
            station_id=s.station_id,
            name=s.name,
            occupancy_time=s.occupancy_time,
            utilization=float(s.utilization),
            units_produced=s.units_produced,
            throughput_rate=round(s.throughput_rate, 2)
        )
        for s in workstations
    ]
    
    return MetricsResponse(factory=factory_data, workers=workers_list, workstations=workstations_list)

@app.post("/worker-events", response_model=EventResponse)
@app.post("/worker-events/", response_model=EventResponse)
async def post_worker_event(event: WorkerEvent, db: Session = Depends(get_db)):
    """Record an event for a specific worker (legacy endpoint)"""
    logger.info(f"📝 Posting event: Worker {event.worker_id}, Type: {event.event_type}, Duration: {event.duration}")
    
    # Validate worker exists
    worker = db.query(WorkerModel).filter(WorkerModel.worker_id == event.worker_id).first()
    if not worker:
        logger.error(f"Worker {event.worker_id} not found")
        return EventResponse(
            success=False,
            message=f"Worker {event.worker_id} not found"
        )
    
    # Log before update
    logger.info(f"Before: Worker {event.worker_id} - Units: {worker.units_produced}, Active Time: {worker.active_time}, Util: {worker.utilization}%")
    
    # Update worker data based on event type
    if event.event_type == "task_start":
        worker.active_time += event.duration if event.duration else 0
        logger.info(f"Task started: Added {event.duration}s to active_time")
    elif event.event_type == "task_end":
        worker.units_produced += 1
        worker.active_time += event.duration if event.duration else 0
        logger.info(f"Task ended: +1 unit, +{event.duration}s active_time")
    elif event.event_type == "break":
        worker.active_time -= event.duration if event.duration else 0
        if worker.active_time < 0:
            worker.active_time = 0
        logger.info(f"Break: Reduced active_time by {event.duration}s")
    elif event.event_type == "error":
        # Errors reduce utilization
        worker.utilization = max(0, worker.utilization - 5)
        logger.info(f"Error: Reduced utilization by 5%")
    
    # Recalculate utilization (0-100%)
    max_time = 3600  # 1 hour max
    worker.utilization = min(100, int((worker.active_time / max_time) * 100))
    
    # Log after update
    logger.info(f"After: Worker {event.worker_id} - Units: {worker.units_produced}, Active Time: {worker.active_time}, Util: {worker.utilization}%")
    
    # Store event record in database
    db_event = WorkerEventModel(
        worker_id=event.worker_id,
        event_type=event.event_type,
        duration=event.duration,
        notes=event.notes
    )
    db.add(db_event)
    db.commit()
    
    logger.info(f"✅ Event saved successfully for Worker {event.worker_id}")
    
    return EventResponse(
        success=True,
        message=f"Event recorded for worker {event.worker_id}"
    )

@app.get("/worker-events")
@app.get("/worker-events/")
async def get_worker_events(worker_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all events or events for a specific worker"""
    query = db.query(WorkerEventModel)
    if worker_id:
        query = query.filter(WorkerEventModel.worker_id == worker_id)
    events = query.all()
    return [
        {
            "worker_id": e.worker_id,
            "event_type": e.event_type,
            "duration": e.duration,
            "notes": e.notes,
            "timestamp": e.timestamp.isoformat()
        }
        for e in events
    ]

@app.post("/events", response_model=EventResponse)
@app.post("/events/", response_model=EventResponse)
async def ingest_ai_event(event: AIEvent, db: Session = Depends(get_db)):
    """Ingest AI-generated events from computer vision system"""
    logger.info(f"Ingesting AI event: Worker {event.worker_id}, Station {event.station_id}, Type: {event.event_type}")
    
    # Check for duplicates
    if is_duplicate(db, event.timestamp, event.worker_id, event.station_id, event.event_type):
        logger.warning(f"Duplicate AI event detected and skipped")
        return EventResponse(success=False, message="Duplicate event detected")
    
    # Validate worker and station exist
    worker = db.query(WorkerModel).filter(WorkerModel.worker_id == event.worker_id).first()
    station = db.query(WorkstationModel).filter(WorkstationModel.station_id == event.station_id).first()
    
    if not worker or not station:
        return EventResponse(success=False, message="Invalid worker or station ID")
    
    # Create and store event in database
    db_event = AIEventModel(
        timestamp=event.timestamp,
        worker_id=event.worker_id,
        station_id=event.station_id,
        event_type=event.event_type,
        confidence=event.confidence,
        count=event.count,
        notes=event.notes
    )
    
    db.add(db_event)
    db.commit()
    
    # Recalculate metrics
    calculate_ai_event_metrics(db)
    
    logger.info(f"✅ AI event processed successfully")
    return EventResponse(success=True, message=f"AI event recorded for worker {event.worker_id}")

@app.get("/events")
@app.get("/events/")
async def get_events(worker_id: Optional[int] = None, station_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get AI events with optional filtering"""
    query = db.query(AIEventModel)
    if worker_id:
        query = query.filter(AIEventModel.worker_id == worker_id)
    if station_id:
        query = query.filter(AIEventModel.station_id == station_id)
    
    # Sort by timestamp
    events = query.order_by(AIEventModel.timestamp).all()
    
    return {
        "events": [
            {
                "timestamp": e.timestamp,
                "worker_id": e.worker_id,
                "station_id": e.station_id,
                "event_type": e.event_type,
                "confidence": e.confidence,
                "count": e.count,
                "notes": e.notes
            }
            for e in events
        ],
        "total_count": len(events)
    }

@app.get("/workers")
async def get_workers(db: Session = Depends(get_db)):
    """Get all workers with metadata"""
    workers = db.query(WorkerModel).all()
    return {
        "workers": [
            {
                "worker_id": w.worker_id,
                "name": w.name,
                "shift": w.shift,
                "active_time": w.active_time,
                "idle_time": w.idle_time,
                "units_produced": w.units_produced,
                "utilization": w.utilization
            }
            for w in workers
        ]
    }

@app.get("/workers/{worker_id}")
async def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get specific worker details"""
    worker = db.query(WorkerModel).filter(WorkerModel.worker_id == worker_id).first()
    if not worker:
        return {"error": f"Worker {worker_id} not found"}
    
    events_count = db.query(AIEventModel).filter(AIEventModel.worker_id == worker_id).count()
    
    return {
        "worker_id": worker.worker_id,
        "name": worker.name,
        "shift": worker.shift,
        "active_time": worker.active_time,
        "idle_time": worker.idle_time,
        "units_produced": worker.units_produced,
        "utilization": worker.utilization,
        "events_count": events_count
    }

@app.get("/workstations")
async def get_workstations(db: Session = Depends(get_db)):
    """Get all workstations with metadata"""
    stations = db.query(WorkstationModel).all()
    return {
        "workstations": [
            {
                "station_id": s.station_id,
                "name": s.name,
                "type": s.type,
                "occupancy_time": s.occupancy_time,
                "utilization": s.utilization,
                "units_produced": s.units_produced,
                "throughput_rate": s.throughput_rate
            }
            for s in stations
        ]
    }

@app.get("/workstations/{station_id}")
async def get_workstation(station_id: int, db: Session = Depends(get_db)):
    """Get specific workstation details"""
    station = db.query(WorkstationModel).filter(WorkstationModel.station_id == station_id).first()
    if not station:
        return {"error": f"Workstation {station_id} not found"}
    
    events_count = db.query(AIEventModel).filter(AIEventModel.station_id == station_id).count()
    
    return {
        "station_id": station.station_id,
        "name": station.name,
        "type": station.type,
        "occupancy_time": station.occupancy_time,
        "utilization": station.utilization,
        "units_produced": station.units_produced,
        "throughput_rate": station.throughput_rate,
        "events_count": events_count
    }

@app.get("/debug/workers")
async def debug_workers(db: Session = Depends(get_db)):
    """DEBUG: Returns current state of all workers"""
    logger.info("🐛 DEBUG: Returning current workers state")
    workers = db.query(WorkerModel).all()
    worker_events_count = db.query(WorkerEventModel).count()
    return {
        "workers": [
            {
                "worker_id": w.worker_id,
                "name": w.name,
                "shift": w.shift,
                "active_time": w.active_time,
                "idle_time": w.idle_time,
                "units_produced": w.units_produced,
                "utilization": w.utilization
            }
            for w in workers
        ],
        "total_events": worker_events_count
    }

@app.get("/debug/state")
async def debug_state(db: Session = Depends(get_db)):
    """DEBUG: Returns current state of all workers and workstations"""
    workers = db.query(WorkerModel).all()
    stations = db.query(WorkstationModel).all()
    ai_events_count = db.query(AIEventModel).count()
    
    return {
        "workers": [
            {
                "worker_id": w.worker_id,
                "name": w.name,
                "active_time": w.active_time,
                "idle_time": w.idle_time,
                "units_produced": w.units_produced,
                "utilization": w.utilization
            }
            for w in workers
        ],
        "workstations": [
            {
                "station_id": s.station_id,
                "name": s.name,
                "occupancy_time": s.occupancy_time,
                "utilization": s.utilization,
                "units_produced": s.units_produced,
                "throughput_rate": s.throughput_rate
            }
            for s in stations
        ],
        "ai_events_count": ai_events_count,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/admin/reset-data", response_model=EventResponse)
async def reset_data():
    """Reset all data to sample state - useful for testing"""
    try:
        reset_sample_data()
        logger.info("✅ Database reset to sample data")
        return EventResponse(
            success=True,
            message="Database reset to sample data successfully. All events cleared, workers and workstations restored."
        )
    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        return EventResponse(
            success=False,
            message=f"Error resetting database: {str(e)}"
        )

@app.post("/test-post/")
async def test_post(request: Request):
    """DEBUG: Simple test endpoint to verify POST works"""
    try:
        body = await request.json()
        logger.info(f"🐛 DEBUG POST received: {body}")
        return {"received": True, "data": body}
    except Exception as e:
        logger.error(f"🐛 DEBUG POST error: {e}")
        return {"received": False, "error": str(e)}

# Serve static frontend files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database when app starts"""
    logger.info("🚀 Starting Factory Dashboard API...")
    init_db()
    logger.info("✅ Application startup complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
