# Factory Dashboard - Deployment & Testing Guide

## Quick Status

✅ **COMPLETED:**
- Backend with 6 workers, 6 workstations, complete AI event schema
- Frontend dashboard with workstation metrics and filtering
- Comprehensive README.md with architecture, metrics, edge cases
- Docker Compose for multi-container deployment
- Separate Dockerfiles for backend and frontend
- Event deduplication and out-of-order handling
- Complete REST API with 8+ endpoints

⚠️ **TODO (Database Integration - Deferred):**
- SQLite persistence layer
- Metric aggregation caching
- User authentication

---

## Testing the System Locally

### 1. Start Backend Only

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test Health Endpoint:**
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### 2. Start Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

**Expected Output:**
```
  VITE v7.3.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

**Access Dashboard:**
- Open http://localhost:5173 in browser
- Should display workers and workstations

### 3. Test API Endpoints

**GET /metrics:**
```bash
curl http://localhost:8000/metrics | python -m json.tool
```

**Expected:** Factory summary + 6 workers + 6 workstations

**POST /events:**
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:30:45Z",
    "worker_id": 1,
    "station_id": 1,
    "event_type": "working",
    "confidence": 0.95,
    "count": 0,
    "notes": "Test working event"
  }'
```

**Expected:** `{"success": true, "message": "AI event recorded for worker 1"}`

**POST /events (Product Count):**
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:35:45Z",
    "worker_id": 2,
    "station_id": 2,
    "event_type": "product_count",
    "confidence": 0.95,
    "count": 5,
    "notes": "5 units produced"
  }'
```

**Expected:** `{"success": true, "message": "AI event recorded for worker 2"}`

**GET /events:**
```bash
curl http://localhost:8000/events | python -m json.tool
```

**Expected:** Array with your 2 events

**GET /events with Filter:**
```bash
curl 'http://localhost:8000/events?worker_id=1' | python -m json.tool
```

**Expected:** Only events for worker 1

**GET /workers:**
```bash
curl http://localhost:8000/workers | python -m json.tool
```

**Expected:** All 6 workers with metadata

**GET /workstations:**
```bash
curl http://localhost:8000/workstations | python -m json.tool
```

**Expected:** All 6 workstations with types

### 4. Test Duplicate Detection

```bash
# Post the same event twice
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:40:45Z",
    "worker_id": 3,
    "station_id": 3,
    "event_type": "idle",
    "confidence": 0.95,
    "count": 0,
    "notes": "Idle event"
  }'

# Second request should return:
# {"success": false, "message": "Duplicate event detected"}
```

### 5. Test Out-of-Order Handling

```bash
# Post events with reversed timestamps
# Then GET /events and verify they're sorted by timestamp

# First event (timestamp 14:30)
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:30:00Z",
    "worker_id": 4,
    "station_id": 4,
    "event_type": "working",
    "confidence": 0.95,
    "count": 0
  }'

# Second event (timestamp 14:45) - posted AFTER first
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:45:00Z",
    "worker_id": 4,
    "station_id": 4,
    "event_type": "working",
    "confidence": 0.95,
    "count": 0
  }'

# Third event (timestamp 14:35) - posted LAST but earlier
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T14:35:00Z",
    "worker_id": 4,
    "station_id": 4,
    "event_type": "idle",
    "confidence": 0.95,
    "count": 0
  }'

# Verify sort order with GET /events
curl 'http://localhost:8000/events?worker_id=4' | python -m json.tool
# Should show: 14:30:00 → 14:35:00 → 14:45:00
```

---

## Testing the Frontend

1. **Navigate to Dashboard:**
   - Should display 4 factory summary cards (productive time, units, rate, utilization)
   - Should display 6 worker cards with names and metrics
   - Should display 6 workstation cards with throughput

2. **Test Filter Controls:**
   - Select "Specific Worker" → choose "Alice Johnson"
   - Should only show Alice's worker card
   - Select "Specific Workstation" → choose "Assembly Line A"
   - Should only show Assembly Line A's station card
   - Select "All Data" → back to normal

3. **Test Post Event Tab:**
   - Click "Post Event" tab
   - Fill form: Select Worker, Station, Event Type
   - For "Product Count" events, enter count
   - Click "Record Event"
   - Should show success message
   - Event should appear in "Event Log" below

4. **Test Auto-Refresh:**
   - Post an event
   - Wait 10 seconds
   - Factory summary numbers should update

---

## Docker Compose Deployment

### Development Mode

```bash
# Start both services
docker-compose up

# In separate terminal, test:
curl http://localhost:8000/health
curl http://localhost:5173

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

**Services:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

### Production Mode

```bash
# Build and run production frontend
docker-compose --profile prod up

# Services:
# - Backend: http://localhost:8000
# - Frontend (Prod): http://localhost:3000
```

**Note:** Production uses optimized build with Vite + Serve

---

## Deployment to Render.com

### Option A: Single Web Service (Existing Dockerfile)

1. Go to Render.com → New → Web Service
2. Connect GitHub repository
3. Set:
   - **Build:** `npm install --prefix frontend && npm run build --prefix frontend`
   - **Start:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Deploy

### Option B: Two Services (Recommended)

**Backend Service:**
1. Create new Web Service
2. Repository: Your repo
3. Root Directory: `backend`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Frontend Service:**
1. Create new Web Service
2. Repository: Your repo
3. Root Directory: `frontend`
4. Build: `npm install && npm run build`
5. Start: `npm run preview -- --host 0.0.0.0 --port $PORT`
6. Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-service.onrender.com`

---

## Database Integration (Future)

When ready to add persistence:

```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./factory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
```

Add to docker-compose:
```yaml
db:
  image: postgres:15
  environment:
    POSTGRES_PASSWORD: factory123
  volumes:
    - postgres-data:/var/lib/postgresql/data
```

---

## Monitoring & Debugging

### Check Backend State
```bash
curl http://localhost:8000/debug/state | python -m json.tool
```

**Output Shows:**
- All 6 workers with current metrics
- All 6 workstations with current metrics
- Total AI events count
- System timestamp

### Check Specific Worker
```bash
curl http://localhost:8000/workers/1 | python -m json.tool
```

### View Event Stream
```bash
curl http://localhost:8000/events | python -m json.tool
```

### Check Backend Logs
```bash
# Development
python main.py  # See INFO logs in terminal

# Docker
docker-compose logs -f backend
```

---

## Performance Testing

### Load Testing with Artillery

```bash
# Install
npm install -g artillery

# Create test file: load-test.yml
targets:
  - name: Factory API
    url: http://localhost:8000

phases:
  - name: "Warm up"
    duration: 10
    arrivalRate: 1

  - name: "Ramp up"
    duration: 30
    arrivalRate: 5

  - name: "Peak"
    duration: 30
    arrivalRate: 10

scenarios:
  - name: "Typical usage"
    flow:
      - get:
          url: "/metrics"
      - post:
          url: "/events"
          json:
            timestamp: "{{ now }}"
            worker_id: "{{ $randomNumber(1, 6) }}"
            station_id: "{{ $randomNumber(1, 6) }}"
            event_type: "working"
            confidence: 0.95
            count: 0

# Run
artillery run load-test.yml
```

---

## Troubleshooting

**Issue: "Port 8000 already in use"**
```bash
# Kill the process
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 9000
```

**Issue: "Module not found: fastapi"**
```bash
pip install -r backend/requirements.txt
```

**Issue: "npm ERR! not ok"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Issue: "CORS Error in browser"**
```bash
# Ensure vite.config.js has proxy:
# /metrics → localhost:8000
# /events → localhost:8000
# /workers → localhost:8000
# /workstations → localhost:8000
```

---

## Checklist for Launch

### Backend
- [x] 6 workers with names
- [x] 6 workstations with types
- [x] AI event model (working, idle, absent, product_count)
- [x] Event endpoints (POST /events, GET /events)
- [x] Worker endpoints (GET /workers, GET /workers/{id})
- [x] Workstation endpoints (GET /workstations, GET /workstations/{id})
- [x] Metrics endpoints (GET /metrics)
- [x] Duplicate detection
- [x] Out-of-order handling
- [x] Error handling

### Frontend
- [x] Dashboard with factory summary
- [x] Worker cards with all metrics
- [x] Workstation cards with all metrics
- [x] Event posting form
- [x] Event log display
- [x] Filter controls (all/worker/workstation)
- [x] Real-time refresh (10 seconds)
- [x] Error states

### Documentation
- [x] Comprehensive README.md
- [x] API Reference with examples
- [x] Data models documented
- [x] Metrics formulas
- [x] Edge case handling
- [x] Scaling discussion
- [x] Deployment instructions

### Deployment
- [x] Dockerfile (single image)
- [x] Docker Compose (multi-service)
- [x] Dockerfile.backend
- [x] Dockerfile.frontend
- [x] Build instructions
- [x] Local testing verified

### Optional (Deferred)
- [ ] SQLite database
- [ ] User authentication
- [ ] Caching layer
- [ ] WebSocket support

---

## Next Steps

1. **Run Locally:** Follow "Testing the System Locally" section
2. **Deploy to Render:** Follow "Deployment to Render.com" section
3. **Monitor:** Use "Monitoring & Debugging" tools to verify
4. **Scale (Future):** Add database when traffic increases

---

**System Status:** ✅ Production Ready (minus database persistence)
**Last Updated:** January 2024
**Version:** 1.0.0
