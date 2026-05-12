import redis
import json
import os
import time
import numpy as np
import onnxruntime as rt
import joblib
import sqlite3

# Konfigurasi
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
QUEUE_NAME = "transaction_queue"
DB_PATH = "data/predictions.db"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_detection_model.onnx")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.joblib")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            transaction_id INTEGER,
            amount REAL,
            prediction TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def start_worker():
    print("🛠️ Initializing Worker...")
    init_db()
    
    # Load Model & Scaler
    scaler = joblib.load(SCALER_PATH)
    sess = rt.InferenceSession(MODEL_PATH)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    prob_name = sess.get_outputs()[1].name

    # Konek Redis
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    
    print("👷 Worker is ready and listening to queue...")
    
    while True:
        # Ambil data dari Redis (Blocking Pop)
        _, message = r.brpop(QUEUE_NAME)
        data = json.loads(message)
        
        # Preprocessing
        amount_scaled = scaler.transform([[data['amount']]])[0][0]
        final_features = data['features_v'] + [amount_scaled]
        input_data = np.array([final_features], dtype=np.float32)
        
        # Predict
        results = sess.run([label_name, prob_name], {input_name: input_data})
        predicted_label = int(results[0][0])
        fraud_probability = float(results[1][0][1])
        
        prediction_text = "FRAUD" if predicted_label == 1 else "NORMAL"
        
        # Simpan ke SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO results (transaction_id, amount, prediction, confidence)
            VALUES (?, ?, ?, ?)
        ''', (data['id'], data['amount'], prediction_text, fraud_probability))
        conn.commit()
        conn.close()
        
        print(f"✅ [Processed] ID: {data['id']} | Result: {prediction_text} ({fraud_probability:.4f})")

if __name__ == "__main__":
    try:
        start_worker()
    except KeyboardInterrupt:
        print("Stopping worker...")
