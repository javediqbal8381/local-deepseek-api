# deepseek_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, BitsAndBytesConfig
import torch
import uvicorn

# Configuration for low-memory environments (1GB RAM)
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
MAX_TOKENS = 80  # Reduce if getting OOM errors
DEVICE = "cpu"  # Force CPU-only for Free Tier compatibility

# Initialize model with quantization
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_skip_modules=["lm_head"]
)

try:
    chatbot = pipeline(
        task="text-generation",
        model=MODEL_NAME,
        device_map=DEVICE,
        torch_dtype=torch.float16,
        # quantization_config=quantization_config,
        model_kwargs={"low_cpu_mem_usage": True}
    )
except Exception as e:
    raise RuntimeError(f"Model loading failed: {str(e)}") from e

# Create FastAPI app
app = FastAPI(title="DeepSeek-R1 Chat API")

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = MAX_TOKENS
    temperature: float = 0.7

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = chatbot(
            request.prompt,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            pad_token_id=chatbot.tokenizer.eos_token_id
        )
        return {"response": response[0]["generated_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run server on port 8000 (make sure EC2 security group allows this)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        timeout_keep_alive=3000  # Needed for slow EC2 responses
    )