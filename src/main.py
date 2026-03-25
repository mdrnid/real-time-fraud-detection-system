import os
import joblib
import numpy as np
import onnxruntime as rt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Inisialisasi Aplikasi
app = FastAPI(
    title="Fraud Detection System API",
    description="API untuk mendeteksi transaksi fraud menggunakan XGBoost & ONNX",
    version="1.0.0"
)

# --- Setup Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_detection_model.onnx")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.joblib")

# --- LOAD MODEL & SCALER (Hanya sekali saat server start) ---
try:
    print("Loading Scaler...")
    scaler = joblib.load(SCALER_PATH)
    
    print("Loading ONNX Model...")
    sess = rt.InferenceSession(MODEL_PATH)
    
    # Dapatkan nama input & output layer secara dinamis
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    # Output ke-2 biasanya adalah probability map (jika zipmap=True/Default)
    prob_name = sess.get_outputs()[1].name 
    
    print(f"Model Loaded! Input: {input_name}, Output: {label_name}")
except Exception as e:
    print(f"CRITICAL ERROR: Gagal load model. {e}")
    sess = None

# --- DEFINISI REQUEST BODY (Data Contract) ---
class TransactionPayload(BaseModel):
    # Kita buat list V1-V28 agar code lebih ringkas
    # User wajib kirim array berisi 28 angka untuk fitur V
    features_v: List[float] 
    amount: float

# --- ENDPOINT UTAMA ---
@app.post("/predict_transaction")
async def predict(payload: TransactionPayload):
    if sess is None:
        raise HTTPException(status_code=500, detail="Model belum siap.")

    # 1. Validasi Input V1-V28
    if len(payload.features_v) != 28:
        raise HTTPException(status_code=400, detail=f"Fitur V harus berjumlah 28. Kamu mengirim {len(payload.features_v)}.")

    try:
        # 2. PREPROCESSING: Scaling Amount
        # Menggunakan RobustScaler yang diload
        amount_scaled = scaler.transform([[payload.amount]])[0][0]

        # 3. MENYUSUN INPUT ARRAY (Production Logic)
        # Gabungkan V1-V28 dengan Amount_Scaled di posisi terakhir
        final_features = payload.features_v + [amount_scaled]
        
        # Konversi ke format Numpy Float32 (Wajib untuk ONNX)
        input_data = np.array([final_features], dtype=np.float32)

        # 4. JALANKAN INFERENSI (PREDIKSI)
        results = sess.run([label_name, prob_name], {input_name: input_data})
        
        predicted_label = int(results[0][0]) # Hasil: 0 atau 1
        
        # --- BAGIAN INI YANG DIPERBAIKI ---
        # ... (kode baru yang Benar)
        probs_array = results[1][0]          # Output: [0.99, 0.01] (Array)
        
        # Ambil index ke-1 (Probabilitas Fraud)
        # Kita pakai index [1] karena urutannya pasti [Prob_Normal, Prob_Fraud]
        fraud_probability = float(probs_array[1])

        # 5. KEMBALIKAN RESPONSE JSON
        return {
            "status": "success",
            "prediction": "FRAUD" if predicted_label == 1 else "NORMAL",
            "confidence_score": fraud_probability, # Sekarang sudah aman
            "details": {
                "raw_amount": payload.amount,
                "amount_scaled": float(amount_scaled),
                "model_version": "v1_xgboost_onnx"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

# --- ROOT ENDPOINT ---
@app.get("/")
def health_check():
    return {"status": "API is Online", "service": "Kredivo Fraud Detector"}