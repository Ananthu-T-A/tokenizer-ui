# Tokenizer Visualizer

A tool to visualize how different tokenizers split text into tokens. Each token is displayed with a unique color based on its token ID.

## Features

- Multiple tokenizer support (GPT-2, Llama, Mistral, Gemma, Qwen, Phi, etc.)
- Real-time tokenization with debouncing
- Color-coded token visualization
- Token count and character count statistics
- Hover over tokens to see their token IDs
- Special character visualization (spaces as ·, newlines as ↵, tabs as →)

## Setup

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Run the backend server:
```bash
uv run python main.py
```

The backend will start on `http://localhost:8000`

### Frontend

1. Open `index.html` in your web browser, or serve it with a simple HTTP server:
```bash
python -m http.server 8080
```

Then visit `http://localhost:8080`

## Usage

1. Start the backend server
2. Open the frontend in your browser
3. Select a tokenizer from the dropdown menu
4. Enter text in the textarea
5. View the tokenized output with color-coded tokens
6. Hover over tokens to see their token IDs

## API Endpoints

- `GET /` - Health check
- `GET /tokenizers` - List available tokenizers
- `POST /tokenize` - Tokenize text
  - Request body: `{"text": "string", "tokenizer_name": "string"}`
  - Response: `{"tokens": [...], "token_count": number}`
