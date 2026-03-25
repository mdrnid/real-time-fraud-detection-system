# 🛡️ Real-time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![ONNX](https://img.shields.io/badge/ML-ONNX_Inference-orange.svg)

An end-to-end Machine Learning solution for detecting fraudulent credit card transactions in real-time. This system features a high-performance **FastAPI** backend using **XGBoost (via ONNX)** and a modern **Streamlit** dashboard for monitoring and manual transaction checks.

## 🚀 Fitur Utama

- **Real-time Inference:** Prediksi instan menggunakan ONNX Runtime untuk latensi minimal.
- **Robust Preprocessing:** Menggunakan `RobustScaler` untuk menangani outlier pada data transaksi finansial.
- **Modern Dashboard:** UI interaktif untuk simulasi input transaksi 28 fitur PCA & Amount.
- **Microservices Ready:** Terbagi menjadi layanan Backend API dan Frontend UI.
- **Containerized:** Deployment mudah menggunakan Docker & Docker Compose.
- **Automated Testing:** Dilengkapi dengan unit & integration tests menggunakan Pytest.

## 🏗️ Arsitektur Teknologi

- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **ML Engine:** XGBoost (dikonversi ke format ONNX)
- **Inference:** ONNX Runtime
- **Containerization:** Docker & Docker Compose
- **Data Validation:** Pydantic

## 🛠️ Instalasi & Penggunaan

### Menggunakan Docker (Rekomendasi)

Pastikan Docker & Docker Compose sudah terinstal di sistem Anda.

1. Clone repository:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. Jalankan sistem:
   ```bash
   docker-compose up --build
   ```

3. Akses aplikasi:
   - **Frontend:** `http://localhost:8501`
   - **Backend API Docs:** `http://localhost:8000/docs`

### Instalasi Lokal

1. Persiapkan Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # atau venv\Scripts\activate di Windows
   ```

2. Instal dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan Backend (FastAPI):
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

4. Jalankan Frontend (Streamlit) di terminal baru:
   ```bash
   streamlit run src/streamlit_app.py
   ```

## 🧠 Detail ML Model

Model dilatih menggunakan dataset transaksi kartu kredit dengan fokus pada **XGBoost Classifier**. Untuk memastikan performa produksi yang optimal, model diekspor ke format **ONNX**. Preprocessing fitur 'Amount' dilakukan menggunakan **RobustScaler** untuk meminimalkan dampak dari nilai transaksi yang ekstrem (outliers).

## 📊 Dokumentasi API

- `POST /predict_transaction`: Menerima 28 fitur PCA dan nominal transaksi. Mengembalikan label (FRAUD/NORMAL) beserta skor kepercayaan (confidence).
- `GET /`: Health check untuk memastikan servis aktif.

## 📜 Lisensi

Proyek ini berada di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---
*Dibuat oleh [Nama Anda/GitHub Username]*
