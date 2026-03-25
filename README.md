# 🛡️ Real-time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![ONNX](https://img.shields.io/badge/ML-ONNX_Inference-orange.svg)

A high-performance, end-to-end Machine Learning solution for detecting fraudulent credit card transactions in real-time. This system utilizes a **FastAPI** backend optimized with **ONNX Runtime** for lightning-fast inference and a modern **Streamlit** dashboard for monitoring and manual simulation.

## 🚀 Key Features

- **Real-time Inference:** Instant predictions using an XGBoost model converted to ONNX for minimal latency.
- **Robust Preprocessing:** Implements `RobustScaler` to handle outliers common in financial transaction data.
- **Interactive Dashboard:** Modern UI for simulating transactions with 28 PCA-transformed features and amount input.
- **Microservices Architecture:** Decoupled Backend API and Frontend UI services.
- **Containerized Deployment:** Seamless setup and scaling using Docker & Docker Compose.
- **Automated Quality Assurance:** Includes integration and unit tests powered by Pytest.

## 🏗️ Technology Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **ML Engine:** XGBoost (Distributed via ONNX)
- **Inference Runtime:** ONNX Runtime
- **DevOps:** Docker & Docker Compose
- **Data Handling:** Pydantic & NumPy

## 🛠️ Installation & Setup

### Dockerized Setup (Recommended)

Ensure you have Docker and Docker Compose installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/mdrnid/real-time-fraud-detection-system.git
   cd real-time-fraud-detection-system
   ```

2. Launch the services:
   ```bash
   docker-compose up --build
   ```

3. Access the applications:
   - **Frontend UI:** `http://localhost:8501`
   - **Interactive API Docs:** `http://localhost:8000/docs`

### Local Development Setup

1. Create a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Backend (FastAPI):
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

4. Start the Frontend (Streamlit) in a separate terminal:
   ```bash
   streamlit run src/streamlit_app.py
   ```

## 🧠 Machine Learning Overview

The system is powered by an **XGBoost Classifier** trained on a credit card fraud dataset sourced from **Kaggle** (Credit Card Fraud Detection 2023). To ensure production-grade performance, the model is served via **ONNX**, enabling sub-millisecond inference. Feature engineering includes **Robust Scaling** for highly skewed transaction amounts, ensuring the model remains accurate even with extreme outliers.

## 📊 API Documentation

- `POST /predict_transaction`: Accepts 28 PCA features and transaction amount. Returns the prediction (FRAUD/NORMAL) and a confidence score.
- `GET /`: Health check endpoint to verify service status.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by [mdrnid](https://github.com/mdrnid)*
