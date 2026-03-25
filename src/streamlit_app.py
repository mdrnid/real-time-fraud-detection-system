import streamlit as st
import requests
import os

st.set_page_config(page_title="Fraud Detection Dashboard", layout="centered")

# Set up the styling
st.title("Real-time Fraud Detection System")
st.write("Enter the transaction details below to check if it's potentially fraudulent. The model uses XGBoost converted to ONNX for lightning-fast inference.")

# Container for input fields
with st.container():
    st.subheader("Transaction Features")
    col1, col2 = st.columns(2)
    
    amount = st.number_input("Transaction Amount (Rupiah)", min_value=0.0, value=150000.0, step=1000.0)
    
    st.markdown("---")
    st.write("**V1 - V28 Features** (These are typically PCA-transformed features from the original dataset to protect privacy)")
    
    # Generate 28 inputs dynamically
    v_features = []
    
    # Create a clean grid for the 28 features (4 columns, 7 rows)
    cols = st.columns(4)
    for i in range(28):
        with cols[i % 4]:
            val = st.number_input(f"V{i+1}", value=0.0, step=0.1, format="%.4f")
            v_features.append(val)

# Submit button
if st.button("🔍 Detect Fraud", type="primary", use_container_width=True):
    # API URL inside the docker network
    api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/predict_transaction")
    
    payload = {
        "features_v": v_features,
        "amount": amount
    }
    
    with st.spinner('Analyzing transaction...'):
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status() 
            result = response.json()
            
            # Display results
            st.markdown("---")
            st.subheader("Prediction Result")
            
            prediction = result['prediction']
            confidence_score = result['confidence_score'] * 100
            
            if prediction == "FRAUD":
                st.error(f"🚨 **FRAUD DETECTED** 🚨")
                st.warning(f"Confidence: {confidence_score:.2f}%")
            else:
                st.success(f"✅ **NORMAL TRANSACTION**")
                st.info(f"Fraud Probability: {confidence_score:.2f}%")
                
            with st.expander("View Raw API Response"):
                st.json(result)
                
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend API. Error: {e}")
