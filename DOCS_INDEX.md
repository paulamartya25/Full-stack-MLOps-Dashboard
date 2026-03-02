# Factory Dashboard - Documentation Index

## 📋 Quick Navigation

### 🚀 Getting Started (5 minutes)
**File:** [QUICKSTART.md](QUICKSTART.md)
- Start backend and frontend
- Docker quick start
- View the dashboard
- Test the API with curl

### 📖 Complete Documentation (Comprehensive)
**File:** [README.md](README.md)
- Full architecture overview
- API reference with examples
- Data models documentation
- Metrics calculation formulas
- Design assumptions
- Edge case handling
- Deployment guide
- Tech stack details

### 🚢 Deployment & Testing (Detailed)
**File:** [DEPLOYMENT.md](DEPLOYMENT.md)
- Step-by-step local testing
- 5+ curl test examples
- Docker Compose deployment
- Render.com deployment (both options)
- Database integration roadmap
- Performance testing with load tools
- Troubleshooting procedures
- Pre-launch checklist

### ✅ Implementation Summary (What Was Built)
**File:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- Complete list of what was implemented
- File structure and locations
- Lines of code added
- Features matrix
- Testing coverage
- Performance characteristics
- Assumptions & design decisions

---

## 📚 Which File Should I Read?

### I want to start immediately
→ Read: **QUICKSTART.md** (5 min read)

### I want to understand how it works
→ Read: **README.md** (20 min read)

### I want to deploy to production
→ Read: **DEPLOYMENT.md** (30 min read)

### I want to see what was built
→ Read: **IMPLEMENTATION_SUMMARY.md** (15 min read)

### I need to troubleshoot
→ Go to: **DEPLOYMENT.md** → Troubleshooting section

### I'm modifying the code
→ Check: **backend/main.py** (417 lines, fully documented)
→ Check: **frontend/src/App.jsx** (React dashboard)
→ Check: **frontend/src/WorkerEvents.jsx** (Event posting form)

---

## 📁 File Locations

### Source Code
```
backend/
  ├── main.py                  ← All API endpoints & logic (417 lines)
  ├── requirements.txt         ← Python dependencies
  └── Dockerfile.backend       ← Container for backend

frontend/
  ├── src/
  │   ├── App.jsx              ← Dashboard page (updated)
  │   ├── WorkerEvents.jsx     ← Event posting (updated)
  │   ├── main.jsx
  │   ├── App.css
  │   └── index.css
  ├── package.json             ← npm dependencies
  ├── vite.config.js           ← Vite config (with API proxy)
  └── Dockerfile.frontend      ← Container for frontend
```

### Configuration
```
docker-compose.yaml             ← Multi-service orchestration
Dockerfile                      ← Single-stage production build
.gitignore                      ← Git ignore rules
```

### Documentation
```
QUICKSTART.md                   ← 5-minute setup guide
README.md                       ← Complete system documentation
DEPLOYMENT.md                   ← Deployment & testing guide
IMPLEMENTATION_SUMMARY.md       ← What was built
this file (Documentation Index)
```

---

## 🔍 Quick Reference

### Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

### Use Docker
```bash
docker-compose up
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

### Test an Endpoint
```bash
curl http://localhost:8000/metrics
curl http://localhost:8000/events
curl http://localhost:8000/health
```

---

## 🎯 Feature Overview

### Backend Features (FastAPI)
✅ 8 REST endpoints  
✅ 6 workers with names  
✅ 6 workstations with types  
✅ AI event ingestion (working, idle, absent, product_count)  
✅ Event deduplication (hash-based)  
✅ Out-of-order event handling  
✅ Real-time metric calculation  
✅ Comprehensive logging  

### Frontend Features (React)
✅ Real-time dashboard (10-second refresh)  
✅ Worker metrics display (6 cards)  
✅ Workstation metrics display (6 cards)  
✅ Filter by worker or workstation  
✅ Event posting form  
✅ Event log with real-time updates  
✅ Responsive design  
✅ Error handling & retry  

### Deployment Features
✅ Docker containerization  
✅ Docker Compose orchestration  
✅ Multi-stage frontend build (dev & prod)  
✅ Health checks  
✅ Volume mounts for live reload  
✅ Environment variable support  

---

## 📊 What Gets Tracked

### Per Worker
- Name
- Shift
- Active time (seconds)
- Idle time (seconds)
- Units produced
- Utilization %

### Per Workstation
- Name
- Type
- Occupancy time (seconds)
- Utilization %
- Units produced
- Throughput rate (units/hour)

### Factory Level
- Total productive time
- Total production count
- Average production rate
- Average utilization

### Events
- Timestamp (ISO 8601)
- Worker ID
- Station ID
- Event type (working, idle, absent, product_count)
- Confidence score
- Unit count (for product_count events)
- Notes

---

## 🔗 API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/metrics` | Factory + worker + station metrics |
| POST | `/events` | Ingest AI event |
| GET | `/events` | Retrieve events (with filtering) |
| GET | `/workers` | List all workers |
| GET | `/workers/{id}` | Get specific worker |
| GET | `/workstations` | List all workstations |
| GET | `/workstations/{id}` | Get specific workstation |
| GET | `/debug/workers` | Debug worker state |
| GET | `/debug/state` | Debug full system state |

---

## 🐛 Debugging Tips

### Check if backend is running
```bash
curl http://localhost:8000/health
```

### View system state
```bash
curl http://localhost:8000/debug/state | python -m json.tool
```

### See backend logs
```bash
python main.py  # Direct logs to terminal
# or
docker-compose logs -f backend  # If using Docker
```

### Check browser console
Open DevTools (F12) → Console tab → Look for errors

### Test API endpoint directly
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
    "notes": "Test"
  }'
```

---

## 🎓 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend API | FastAPI | 0.100+ |
| Backend HTTP | Uvicorn | 0.20+ |
| Frontend | React | 19+ |
| Frontend Build | Vite | 7.3+ |
| Frontend CSS | Tailwind CSS | 4.2+ |
| Python Runtime | Python | 3.9+ |
| Node Runtime | Node.js | 22+ |
| Containers | Docker | 20.10+ |
| Orchestration | Docker Compose | 2.0+ |

---

## ✨ Key Highlights

1. **6 Real Workers:** Named workers with shifts and complete metrics
2. **6 Real Workstations:** Fully equipped with types and throughput tracking
3. **Comprehensive Metrics:** Active time, idle time, production, utilization
4. **Smart Event Processing:** Duplicate detection + out-of-order handling
5. **Professional UI:** Responsive design with real-time updates
6. **Production Ready:** Docker-ready, fully documented, deployable

---

## 🚀 Deployment Paths

### Local Development
→ Follow: QUICKSTART.md

### Docker Local
→ Follow: QUICKSTART.md → Option 2

### Render.com Cloud
→ Follow: DEPLOYMENT.md → "Deployment to Render.com"

### Self-Hosted
→ Follow: DEPLOYMENT.md → "Docker Compose Deployment"

---

## 📋 Pre-Launch Checklist

- [ ] Backend runs without errors: `python main.py`
- [ ] Frontend runs without errors: `npm run dev`
- [ ] Dashboard loads at http://localhost:5173
- [ ] All 6 workers visible
- [ ] All 6 workstations visible
- [ ] Can post event from UI
- [ ] Event appears in log immediately
- [ ] Can filter by worker
- [ ] Can filter by workstation
- [ ] Metrics update every 10 seconds
- [ ] Metrics change after events
- [ ] No browser console errors
- [ ] Docker Compose works: `docker-compose up`
- [ ] No Python errors
- [ ] No npm errors

---

## 📞 Support Matrix

| Question | Resource |
|----------|----------|
| How do I start? | QUICKSTART.md |
| How does it work? | README.md |
| How do I deploy? | DEPLOYMENT.md |
| What was built? | IMPLEMENTATION_SUMMARY.md |
| How do I fix X? | DEPLOYMENT.md → Troubleshooting |
| API reference? | README.md → API Reference |
| Metrics formulas? | README.md → Metrics Calculation |
| Architecture? | README.md → Architecture |

---

## 🎉 You Have Everything

✅ Complete backend  
✅ Complete frontend  
✅ Working dashboard  
✅ Event ingestion  
✅ Metric tracking  
✅ Docker setup  
✅ Comprehensive docs  
✅ Testing guide  
✅ Deployment guide  

**Ready to go!** Pick a doc above based on what you need.

---

**Factory Dashboard** | Version 1.0.0 | January 2024
