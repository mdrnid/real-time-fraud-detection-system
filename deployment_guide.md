# Deployment Guide: Fraud Detection System

This guide explains how to deploy your containerized Machine Learning system to the cloud. As an ML Engineer, being able to point a recruiter to a live URL is your strongest portfolio asset.

## Option 1: Render.com (Easiest - Recommended)
Render is excellent because it supports `docker-compose` and is very designer/engineer friendly.

1. **Push your code to GitHub**: Create a private or public repository and push all your files (including `Dockerfile`, `docker-compose.yml`, `src/`, and `models/`).
2. **Connect to Render**:
   - Create a new **Web Service** on Render.
   - Connect your GitHub repository.
   - Render will detect your `Dockerfile`.
3. **Set Environment Variables**:
   - In the Render dashboard, set `API_URL` for the frontend service to the internal URL provided by Render for your API service.
4. **Deploy**: Render will automatically build your Docker images and provide a public `.onrender.com` URL.

## Option 2: AWS App Runner (Enterprise Standard)
This is what large companies use. It is fully managed and scales automatically.

1. **Push Image to ECR**: Push your built Docker images to **Amazon Elastic Container Registry (ECR)**.
2. **Create App Runner Service**: Point App Runner to your ECR image.
3. **Configuration**: Set the port to 8000 (for API) or 8501 (for Frontend).

## Option 3: Google Cloud Run
Highly professional and "Serverless." You only pay when someone actually uses your API.

1. **Build and Tag**: `docker tag fraud-detection-api gcr.io/your-project/api`
2. **Push**: `docker push gcr.io/your-project/api`
3. **Deploy**: Use `gcloud run deploy` to launch the container.

---

### MLOps Tip: 
Before deploying, ensure your `models/` directory contains the latest `onnx` and `joblib` files. In a mature MLOps pipeline, these would be pulled from a Model Registry (like MLflow or AWS S3) during the build process.
