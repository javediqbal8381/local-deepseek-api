DeepSeek-R1 Chat API

This repository provides a FastAPI-based REST API for interacting with the DeepSeek-R1-Distill-Qwen-1.5B text-generation model. if you want to use higher models then change the name of model. It is optimized for low-memory environments and can run on CPU-only machines.

Features

Simple REST API for text generation.

Runs on CPU (no GPU required).

Uses FastAPI for fast and efficient request handling.

Optimized for low-memory environments.

Installation

1️⃣ Clone the Repository

git clone https://github.com/javediqbal8381/local-deepseek-api.git
cd deepseek-api

2️⃣ Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv/scripts/activate    # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

Running the API

1️⃣ Start the FastAPI Server

uvicorn app:app --host 0.0.0.0 --port 3000

The API will be available at: http://0.0.0.0:3000

2️⃣ Send a Request

Use cURL or Postman to test the API:

curl -X POST "http://0.0.0.0:3000/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?", "max_tokens": 50, "temperature": 0.3}'

Expected Response:

{
    "response": "Hello! I am doing great. How can I assist you today?"
}
