# 🛡️ Real-time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)
![Redis](https://img.shields.io/badge/Redis-Latest-red.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![ONNX](https://img.shields.io/badge/ML-ONNX_Inference-orange.svg)

A high-performance, end-to-end Machine Learning solution for detecting fraudulent credit card transactions in real-time. This system features a robust **Streaming Pipeline** using Redis and a dedicated Worker node for high-throughput fraud analytics.

## 🏗️ System Architecture

The project has evolved from a simple request-response API to a distributed streaming architecture:

1.  **Producer:** Simulates a live stream of transactions from a CSV dataset, pushing payloads into a **Redis Queue**.
2.  **Message Broker (Redis):** Acts as a high-speed buffer to handle transaction bursts.
3.  **Worker Node:** Consumes transactions from Redis, runs **ONNX-optimized XGBoost inference**, and persists results to **SQLite**.
4.  **Live Dashboard:** A minimalist, professional Streamlit console that monitors the database and visualizes fraud metrics in real-time.

## 🚀 Key Features

-   **Asynchronous Streaming:** Decoupled data ingestion and processing for high scalability.
-   **ONNX Optimization:** Model inference is served via ONNX Runtime for sub-millisecond latency.
-   **Real-time Monitoring:** Automated dashboard refresh providing instant visibility into system throughput and fraud rates.
-   **Dual-Mode Analysis:** Supports both autonomous stream monitoring and manual transaction auditing.
-   **Containerized Orchestration:** Full infrastructure (API, UI, Redis) managed via Docker Compose.

## 🛠️ Technology Stack

-   **Backend:** FastAPI (Python)
-   **Broker:** Redis
-   **Processing:** Python Worker (ONNX Runtime)
-   **Frontend:** Streamlit (Minimalist Fintech UI)
-   **ML Engine:** XGBoost (Exported to ONNX)
-   **Database:** SQLite (Result Persistence)
-   **DevOps:** Docker & Docker Compose

## 📦 Installation & Setup

### Dockerized Setup (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/mdrnid/real-time-fraud-detection-system.git
   cd real-time-fraud-detection-system
   ```

2. Launch the infrastructure:
   ```bash
   docker-compose up --build -d
   ```

3. Start the Streaming Pipeline:
   ```bash
   # Terminal 1: Start the Worker
   python src/worker.py

   # Terminal 2: Start the Producer (Simulated Stream)
   python src/producer.py
   ```

4. Access the applications:
   - **Live Monitoring Dashboard:** `http://localhost:8501`
   - **Backend API Docs:** `http://localhost:8000/docs`

## 🧠 Machine Learning Overview

The system uses an **XGBoost Classifier** trained on the Credit Card Fraud Detection 2023 dataset. The model is converted to **ONNX** to eliminate Python overhead during inference. Data is pre-processed using `RobustScaler` to ensure stability against the high variance typical of financial transactions.

---
*Developed by [mdrnid](https://github.com/mdrnid)*
