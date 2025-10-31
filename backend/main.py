from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoProcessor
from typing import List, Dict, Optional
from PIL import Image
import colorsys
import base64
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizers_cache = {}
processors_cache = {}

AVAILABLE_TOKENIZERS = [
    "gpt2",
    "mistralai/Mistral-7B-v0.1",
    "google/gemma-2-2b",
    "Qwen/Qwen2.5-7B",
    "microsoft/phi-2",
    "bert-base-uncased",
    "facebook/opt-125m",
]

MULTIMODAL_TOKENIZERS = [
    "Qwen/Qwen2-VL-2B-Instruct",
]

class ContentPart(BaseModel):
    type: str  # "text" or "image"
    text: Optional[str] = None
    image: Optional[str] = None  # base64 encoded image

class TokenizeRequest(BaseModel):
    text: Optional[str] = None
    content: Optional[List[ContentPart]] = None  # For multimodal input
    tokenizer_name: str = "gpt2"

class TokenInfo(BaseModel):
    token: str
    token_id: int
    color: str
    type: str = "text"  # "text", "image", or "special"

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

def get_processor(tokenizer_name: str):
    if tokenizer_name not in processors_cache:
        try:
            processors_cache[tokenizer_name] = AutoProcessor.from_pretrained(tokenizer_name)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to load processor: {str(e)}")
    return processors_cache[tokenizer_name]

def is_multimodal(tokenizer_name: str) -> bool:
    return tokenizer_name in MULTIMODAL_TOKENIZERS

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
    return {
        "tokenizers": AVAILABLE_TOKENIZERS,
        "multimodal_tokenizers": MULTIMODAL_TOKENIZERS
    }

@app.post("/tokenize", response_model=TokenizeResponse)
def tokenize(request: TokenizeRequest):
    try:
        # Handle multimodal tokenization
        if is_multimodal(request.tokenizer_name) and request.content:
            return tokenize_multimodal(request)

        # Handle text-only tokenization
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is required for text-only tokenizers")

        tokenizer = get_tokenizer(request.tokenizer_name)
        encoded = tokenizer.encode(request.text)

        tokens_info = []
        for idx, token_id in enumerate(encoded):
            token_str = tokenizer.decode([token_id])
            color = generate_color(token_id, len(encoded))
            tokens_info.append(TokenInfo(
                token=token_str,
                token_id=token_id,
                color=color,
                type="text"
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

def tokenize_multimodal(request: TokenizeRequest):
    processor = get_processor(request.tokenizer_name)

    # Build messages in the format expected by Qwen2-VL
    messages = [{"role": "user", "content": []}]

    for part in request.content:
        if part.type == "text":
            messages[0]["content"].append({"type": "text", "text": part.text})
        elif part.type == "image":
            # Decode base64 image
            image_data = base64.b64decode(part.image.split(",")[1] if "," in part.image else part.image)
            image = Image.open(io.BytesIO(image_data))
            messages[0]["content"].append({"type": "image", "image": image})

    # Apply chat template and tokenize
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs = [part["image"] for msg in messages for part in msg["content"] if part.get("type") == "image"]

    inputs = processor(
        text=[text],
        images=image_inputs if image_inputs else None,
        return_tensors="pt",
        padding=True
    )

    input_ids = inputs["input_ids"][0].tolist()

    # Decode tokens and identify image tokens
    tokens_info = []
    image_token_id = processor.tokenizer.convert_tokens_to_ids("<|image_pad|>") if hasattr(processor, 'tokenizer') else None

    # Group consecutive image tokens
    idx = 0
    while idx < len(input_ids):
        token_id = input_ids[idx]
        token_str = processor.tokenizer.decode([token_id])
        color = generate_color(token_id, len(input_ids))

        # Check if this is an image token
        if image_token_id and token_id == image_token_id:
            # Count consecutive image tokens
            image_token_count = 1
            start_idx = idx
            idx += 1
            while idx < len(input_ids) and input_ids[idx] == image_token_id:
                image_token_count += 1
                idx += 1

            # Create a single grouped token for all consecutive image tokens
            tokens_info.append(TokenInfo(
                token=f"IMAGE ({image_token_count} tokens)",
                token_id=image_token_id,
                color=generate_color(image_token_id, len(input_ids)),
                type="image"
            ))
        else:
            # Determine token type for non-image tokens
            if token_str.startswith("<|") and token_str.endswith("|>"):
                token_type = "special"
            else:
                token_type = "text"

            tokens_info.append(TokenInfo(
                token=token_str,
                token_id=token_id,
                color=color,
                type=token_type
            ))
            idx += 1

    return TokenizeResponse(
        tokens=tokens_info,
        token_count=len(input_ids)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
