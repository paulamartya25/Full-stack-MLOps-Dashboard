# Factory Dashboard - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Local Development (Easiest)

**Terminal 1 - Start Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
# Dashboard ready at http://localhost:8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm install
npm run dev
# Dashboard ready at http://localhost:5173
```

**Open Browser:** http://localhost:5173

---

## 🐳 Option 2: Docker (No Python/Node Setup)

```bash
# Start everything in one command
docker-compose up

# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

**Stop:** `docker-compose down`

---

## 📊 What You'll See

### Dashboard Tab
- **Factory Summary:** 4 metrics cards
- **Worker Metrics:** 6 worker cards with utilization bars
- **Workstation Metrics:** 6 station cards with throughput rates
- **Filter Controls:** Filter by specific worker or workstation

### Post Event Tab
- **Form Fields:**
  - Select your Worker (1-6)
  - Select your Workstation (1-6)
  - Event Type: working, idle, absent, or product_count
  - Notes (optional)
- **Event Log:** Shows all events posted in real-time

---

## 🧪 Testing the API (Optional)

### Check Backend Health
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Get Metrics
```bash
curl http://localhost:8000/metrics | python -m json.tool
```

### Post an Event
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
    "notes": "Test event"
  }'
# Response: {"success": true, "message": "AI event recorded for worker 1"}
```

### Get Events
```bash
curl http://localhost:8000/events | python -m json.tool
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip: command not found` | Install Python 3.9+ |
| `npm: command not found` | Install Node.js 22+ |
| Port 8000 in use | Kill process: `lsof -i :8000 && kill -9 <PID>` |
| Port 5173 in use | Kill process: `lsof -i :5173 && kill -9 <PID>` |
| `ModuleNotFoundError` | Run: `pip install -r backend/requirements.txt` |
| `npm ERR!` | Run: `cd frontend && rm -rf node_modules && npm install` |
| Backend not responding | Check: `curl http://localhost:8000/health` |
| Can't reach API from frontend | Config is auto-proxied in dev mode |

---

## 📁 Project Structure

```
factory-dashboard/
├── backend/          ← FastAPI server
│   ├── main.py       ← All endpoints & logic
│   └── requirements.txt
├── frontend/         ← React dashboard
│   ├── src/
│   │   ├── App.jsx   ← Dashboard page
│   │   └── WorkerEvents.jsx ← Event posting page
│   └── package.json
├── README.md         ← Full documentation
└── DEPLOYMENT.md     ← Detailed deployment guide
```

---

## 📚 System Components

### Backend (FastAPI)
- **6 Workers:** Alice Johnson, Bob Smith, Carlos Martinez, Diana Lee, Ethan Brown, Fiona Garcia
- **6 Workstations:** Assembly Lines A/B, Quality Check, Packaging, Testing, Finishing
- **Event Types:** working, idle, absent, product_count

### Frontend (React)
- **Dashboard:** View all metrics and workers
- **Filter:** Select specific worker or workstation
- **Post Event:** Submit events from AI system
- **Event Log:** See all events in real-time

### Features
- ✅ Real-time metrics (updates every 10 seconds)
- ✅ Duplicate event detection
- ✅ Out-of-order event handling
- ✅ Worker & workstation filtering
- ✅ Responsive design
- ✅ Error handling with retry

---

## 🎯 Common Tasks

### View Worker Metrics
1. Click **Dashboard** tab
2. See worker cards with:
   - Active time (seconds)
   - Idle time (seconds)
   - Units produced
   - Utilization %

### Filter by Worker
1. Click **Dashboard** tab
2. Change "View" dropdown to "Specific Worker"
3. Select worker from dropdown
4. Dashboard updates to show only that worker

### Post a Production Event
1. Click **Post Event** tab
2. Select worker and workstation
3. Choose event type: "working" or "product_count"
4. For product counts, enter the number
5. Click "Record Event"
6. See it appear in the event log

### Check System Status
1. Open terminal
2. Run: `curl http://localhost:8000/debug/state`
3. See current state of all workers and workstations

---

## 🚀 Deployment

### Deploy to Render.com (Free Tier Available)

1. Push to GitHub
2. Go to render.com → New → Web Service
3. Select your repository
4. Set build: `npm install --prefix frontend && npm run build --prefix frontend`
5. Set start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Click Deploy

See `DEPLOYMENT.md` for detailed instructions.

---

## 📖 Documentation Files

- **README.md** - Complete system documentation
- **DEPLOYMENT.md** - Deep deployment guide with testing
- **IMPLEMENTATION_SUMMARY.md** - What was built and why
- **This File** - Quick start guide

---

## 🔐 Default Setup (Security Note)

Current setup has CORS enabled for all origins. For production:

```python
# In backend/main.py, change:
allow_origins=["*"]

# To:
allow_origins=["https://yourdomain.com"]
```

---

## 📊 Key Metrics You're Tracking

### Per Worker
- Active time working (seconds)
- Time idle (seconds)
- Units produced
- Utilization % (active / total time)

### Per Workstation
- Occupancy time (seconds)
- Units produced
- Throughput rate (units/hour)
- Utilization %

### Factory Level
- Total productive time (all workers)
- Total units produced
- Average production rate
- Average utilization across workers

---

## ✅ Quick Checklist

Before declaring success:

- [ ] Backend starts without errors: `python main.py`
- [ ] Frontend starts without errors: `npm run dev`
- [ ] Dashboard loads at http://localhost:5173
- [ ] Dashboard shows all 6 workers
- [ ] Dashboard shows all 6 workstations
- [ ] Can post event from UI
- [ ] Event appears in event log immediately
- [ ] Can filter by worker
- [ ] Can filter by workstation
- [ ] Metrics update automatically every 10 seconds
- [ ] Metrics change after posting events
- [ ] No console errors in browser dev tools
- [ ] Docker Compose starts both services: `docker-compose up`

---

## 🎓 Learning Resources

### FastAPI
- Backend code: `backend/main.py`
- Endpoints: GET /metrics, POST /events, GET /workers, GET /workstations

### React
- Main app: `frontend/src/App.jsx`
- Event form: `frontend/src/WorkerEvents.jsx`
- Uses hooks: useState, useEffect
- Uses Axios for API calls

### Docker
- Single container: `Dockerfile`
- Multi-container: `docker-compose.yaml`
- Backend container: `backend/Dockerfile.backend`
- Frontend container: `frontend/Dockerfile.frontend`

---

## 💡 Tips & Tricks

### See Backend Logs
```bash
python main.py  # See logs in terminal
# or
docker-compose logs -f backend  # If using Docker
```

### Test Event Processing
```bash
# Post same event twice - second should fail with duplicate error
curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '...'
curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '...'
```

### View Full System State
```bash
curl http://localhost:8000/debug/state | python -m json.tool
```

### Monitor in Real Time
```bash
# Watch metrics update in real time
watch -n 1 'curl -s http://localhost:8000/metrics | python -m json.tool | head -20'
```

### Check All Endpoints
```bash
curl http://localhost:8000/openapi.json | python -m json.tool
# or
curl http://localhost:8000/docs  # Interactive API docs in browser
```

---

## 🎯 Next Steps

1. **Get it running:** Follow Option 1 or 2 above
2. **Explore the UI:** Post some events, see metrics update
3. **Test the API:** Try the curl examples above
4. **Read the docs:** Check README.md for full reference
5. **Deploy:** Follow DEPLOYMENT.md for Render.com setup

---

## ❓ FAQs

**Q: Can I run this without Python?**  
A: Yes! Use Docker: `docker-compose up`

**Q: Can I run this without Node.js?**  
A: Yes! Docker includes both. Or compile frontend locally with `npm run build`

**Q: Is there a admin panel?**  
A: No, the dashboard is the admin panel. See all data in real-time.

**Q: Where is data stored?**  
A: Currently in memory (RAM). Restarts lose data. Database coming in Phase 2.

**Q: Can I use this with real AI cameras?**  
A: Yes! Have cameras POST to `http://your-server:8000/events` with the JSON format shown.

**Q: How do I deploy to production?**  
A: See DEPLOYMENT.md - Render.com recommended (free tier available)

---

## 🎉 You're Ready!

Your factory monitoring system is ready to use. Start with:

```bash
cd backend && python main.py    # Terminal 1
cd frontend && npm run dev       # Terminal 2
# Open http://localhost:5173
```

**Questions?** See README.md or DEPLOYMENT.md for detailed information.

**Having issues?** Check the Troubleshooting section above or DEPLOYMENT.md.

---

**Happy monitoring! 🏭📊**
