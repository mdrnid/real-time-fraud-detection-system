import joblib
from sklearn.preprocessing import RobustScaler

# In a real training pipeline, we would fit this on X_train. 
# Here we initialize it with the known parameters from the notebook.
scaler = RobustScaler()

# Robust scaler logic: (X - median) / IQR
# We know from the original code:
# Median = 12030.15 
# IQR = 11981.437500000002 
scaler.center_ = [12030.15]
scaler.scale_ = [11981.437500000002]

import os

# Create the models directory if it doesn't exist just in case
os.makedirs('models', exist_ok=True)

joblib.dump(scaler, 'models/scaler.joblib')
print("Scaler saved to models/scaler.joblib successfully.")
