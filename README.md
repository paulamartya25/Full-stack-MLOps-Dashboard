# Factory Productivity AI Dashboard 🏭

A full-stack MLOps solution featuring a FastAPI backend and React frontend to visualize worker productivity.

## 🚀 How to Run (Local Setup)
1. **Backend**: Navigate to `/backend`, activate `venv`, and run `uvicorn main:app --reload`.
2. **Frontend**: Navigate to `/frontend` and run `npm run dev`.
3. **Access**: View the dashboard at `http://localhost:5173`.

## 🗄️ Assumptions & Schema
* **Metric Assumption**: Each "working" or "idle" event represents a **300-second (5-minute)** activity window for productivity calculations.
* **Database**: SQLite tracks workers, workstations, and AI-generated events including confidence scores.

## 🧠 MLOps & Scaling (Theoretical Answers)

### 1. Model Versioning & Drift
* **Versioning**: Use **MLflow** or **DVC** to track which model version generated each productivity event.
* **Drift**: We monitor the `confidence` field in our `events` table. A drop in average confidence over time indicates **Data Drift** (e.g., changes in factory lighting).

### 2. Retraining Strategy
* **Trigger**: Retrain when confidence drops below 0.75 or accuracy falls below KPIs.
* **Process**: Collect low-confidence samples for human labeling and fine-tune via a CI/CD pipeline.

### 3. Scaling the System
* **100+ Cameras**: Replace SQLite with **PostgreSQL** and use **Kafka** for high-throughput event ingestion.
* **Multi-site**: Use **Edge computing** to process video locally, sending only the small JSON metadata to the central cloud dashboard to save bandwidth.