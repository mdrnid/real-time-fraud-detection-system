import requests
import random

# URL API lokal kamu
url = "http://127.0.0.1:8000/predict_transaction"

# 1. Generate Dummy Data (V1-V28 acak)
dummy_v_features = [random.uniform(-2.0, 2.0) for _ in range(28)]

# 2. Siapkan Payload Data
data_transaksi = {
    "features_v": dummy_v_features,
    "amount": 150000.0  # Amount Rupiah Mentah (belum di-scale)
}

# 3. Kirim Request ke API
try:
    response = requests.post(url, json=data_transaksi)
    
    if response.status_code == 200:
        result = response.json()
        print("=== HASIL PREDIKSI ===")
        print(f"Status      : {result['prediction']}")
        print(f"Confidence  : {result['confidence_score'] * 100:.2f}%")
        print(f"Debug Info  : {result['details']}")
    else:
        print("Error:", response.text)

except Exception as e:
    print(f"Koneksi Gagal: {e}")