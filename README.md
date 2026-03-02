# Factory Productivity AI Dashboard 🏭

A full-stack MLOps solution featuring a FastAPI backend and React frontend to visualize worker productivity.

## 🏗️ 1. Architecture Overview
* **Edge (AI Cameras)**: Edge devices run computer vision models to detect worker actions and send lightweight JSON metadata payloads to the backend.
* **Backend (FastAPI)**: Ingests the JSON payloads, processes the business/productivity logic, and stores records in the database.
* **Dashboard (React)**: Fetches aggregated metrics via REST API and visualizes them in a real-time UI.

## 🚀 2. How to Run (Local Setup)
1. **Backend**: Navigate to `/backend`, activate `venv`, and run `uvicorn main:app --reload`.
2. **Frontend**: Navigate to `/frontend` and run `npm run dev`.
3. **Docker (Alternative)**: Run `docker build -t factory-app .` followed by `docker run -p 8000:8000 factory-app`.
4. **Access**: View the dashboard at `http://localhost:5173`.

## 🗄️ 3. Database Schema & Metric Definitions
* **Schema**: SQLite tracks workers, workstations, and an `AIEvent` table (logging timestamp, worker_id, event_type, confidence, and count).
* **Metric Definitions**:
  * **Active Time**: Calculated from "working" events.
  * **Units Produced**: Tracked via "product_count" events, strictly summing the `count` field.

## ⚖️ 4. Assumptions & Tradeoffs
* **Assumption**: Each "working" or "idle" event represents a static **300-second (5-minute)** activity window for productivity calculations.
* **Tradeoff**: We chose SQLite for rapid local development and zero-config setup. The tradeoff is lower write-concurrency, which would bottleneck a real, high-throughput factory environment.

## ⚠️ 5. Handling Data Edge Cases
* **Intermittent Connectivity**: Edge devices buffer events locally in memory or disk. Upon reconnection, the edge device pushes the queued payloads to the backend.
* **Duplicate Events**: Handled via idempotency. The backend checks for a unique combination of (`timestamp` + `worker_id` + `event_type`). Exact matches are dropped.
* **Out-of-order Timestamps**: The backend does not rely on API ingestion time. Metrics are calculated by querying and sorting events by their actual recorded payload `timestamp`.

## 🧠 6. MLOps & Scaling (Theoretical Answers)

### Model Versioning & Drift
* **Versioning**: Use **MLflow** or **DVC** to track which model version generated each productivity event.
* **Drift**: We monitor the `confidence` field in our `events` table. A drop in average confidence over time indicates **Data Drift** (e.g., changes in factory lighting).

### Retraining Strategy
* **Trigger**: Retrain when confidence drops below 0.75 or accuracy falls below KPIs.
* **Process**: Collect low-confidence samples for human labeling and fine-tune via a CI/CD pipeline.

### Scaling the System
* **100+ Cameras**: Replace SQLite with **PostgreSQL** for concurrency and use **Apache Kafka** for high-throughput event ingestion.
* **Multi-site**: Use **Edge computing** (e.g., NVIDIA Jetson) to process video locally, sending only the small JSON metadata to the central cloud dashboard to save bandwidth.