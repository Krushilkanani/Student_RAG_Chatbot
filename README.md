# RAG Chatbot

BM25 top-N + cosine top-N (union) -> zerank-1-small reranker -> confidence threshold -> OpenAI LLM.

## Setup on any laptop

```
git clone <your-repo-url>
cd <repo-folder>
```

1. **Create and activate a virtual environment**
   - Windows (PowerShell): `python -m venv .venv` then `.venv\Scripts\Activate.ps1`
     (if blocked: `Set-ExecutionPolicy -Scope Process Bypass`)
   - Linux / macOS: `python3 -m venv .venv` then `source .venv/bin/activate`
2. **Install** (picks the right PyTorch for this machine): `python install.py`
3. **Create `.env`**: copy `.env.example` to `.env` and put in your `OPENAI_API_KEY`.
   - No GPU, or under 6 GB VRAM: set `RERANK_DEVICE=cpu` and `CANDIDATES_PER_METHOD=10`.
4. **Embed the data once per machine**: `python ingest.py processed_data`
5. **Run**: `python run_all.py`, wait for "Reranker loaded on ...", then open http://127.0.0.1:8000

The first run downloads the reranker (~3.5 GB) on each machine.
Never commit `.env` (it is in `.gitignore`).
