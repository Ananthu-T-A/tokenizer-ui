from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer
from typing import List, Dict
import colorsys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizers_cache = {}

AVAILABLE_TOKENIZERS = [
    "gpt2",
    "mistralai/Mistral-7B-v0.1",
    "google/gemma-2-2b",
    "Qwen/Qwen2.5-7B",
    "microsoft/phi-2",
    "bert-base-uncased",
    "facebook/opt-125m",
]

class TokenizeRequest(BaseModel):
    text: str
    tokenizer_name: str = "gpt2"

class TokenInfo(BaseModel):
    token: str
    token_id: int
    color: str

class TokenizeResponse(BaseModel):
    tokens: List[TokenInfo]
    token_count: int

def get_tokenizer(tokenizer_name: str):
    if tokenizer_name not in tokenizers_cache:
        try:
            tokenizers_cache[tokenizer_name] = AutoTokenizer.from_pretrained(tokenizer_name)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to load tokenizer: {str(e)}")
    return tokenizers_cache[tokenizer_name]

def generate_color(token_id: int, total_tokens: int) -> str:
    hue = (token_id * 137.508) % 360 / 360
    saturation = 0.6
    lightness = 0.75
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

@app.get("/")
def root():
    return {"message": "Tokenizer API is running"}

@app.get("/tokenizers")
def list_tokenizers():
    return {"tokenizers": AVAILABLE_TOKENIZERS}

@app.post("/tokenize", response_model=TokenizeResponse)
def tokenize(request: TokenizeRequest):
    try:
        tokenizer = get_tokenizer(request.tokenizer_name)

        encoded = tokenizer.encode(request.text)

        tokens_info = []
        for idx, token_id in enumerate(encoded):
            token_str = tokenizer.decode([token_id])
            color = generate_color(token_id, len(encoded))
            tokens_info.append(TokenInfo(
                token=token_str,
                token_id=token_id,
                color=color
            ))

        return TokenizeResponse(
            tokens=tokens_info,
            token_count=len(encoded)
        )
    except Exception as e:
        import traceback
        print(f"Error in tokenize: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
