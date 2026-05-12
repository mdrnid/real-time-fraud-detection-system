import pandas as pd
import redis
import json
import time
import os

# Konfigurasi Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
QUEUE_NAME = "transaction_queue"

def start_producer(file_path, limit=100, delay=2):
    """
    Membaca data dari CSV dan mengirimkannya ke antrian Redis.
    """
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        # Test koneksi
        r.ping()
        print(f"✅ Terkoneksi ke Redis di {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        print(f"❌ Gagal konek ke Redis: {e}")
        return

    print(f"📖 Membaca data dari {file_path}...")
    # Baca hanya beberapa baris awal untuk simulasi agar cepat
    df = pd.read_csv(file_path, nrows=limit)
    
    print(f"🚀 Memulai simulasi streaming (Infinite Loop, delay {delay}s)...")
    
    while True:
        for index, row in df.iterrows():
            # Mengambil V1 sampai V28 secara eksplisit berdasarkan nama kolom
            v_features = [float(row[f'V{i}']) for i in range(1, 29)]
            
            payload = {
                "id": int(row.get('id', index)),
                "features_v": v_features,
                "amount": float(row['Amount']),
                "timestamp": time.time()
            }
            
            r.lpush(QUEUE_NAME, json.dumps(payload))
            print(f"📤 [Sent] ID: {payload['id']} | Amount: {payload['amount']}")
            time.sleep(delay)
        
        print("🔄 Loop selesai, mengulang dari awal data...")

if __name__ == "__main__":
    DATA_PATH = "data/creditcard_2023.csv"
    if os.path.exists(DATA_PATH):
        start_producer(DATA_PATH)
    else:
        print(f"❌ File {DATA_PATH} tidak ditemukan.")
