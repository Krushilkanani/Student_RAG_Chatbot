# One-command installer: picks the right PyTorch for this computer, then installs the rest.
# Usage (with the virtual environment activated):   python install.py
import platform
import shutil
import subprocess
import sys

if sys.prefix == sys.base_prefix:
    sys.exit("Activate your virtual environment first (see README), then run this again.")


def pip(*args):
    subprocess.check_call([sys.executable, "-m", "pip", *args])


def nvidia_gpu():
    """Returns (name, VRAM in MiB) or None."""
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], text=True)
        name, mem = [x.strip() for x in out.strip().splitlines()[0].split(",")]
        return name, int(mem)
    except Exception:
        return None


info = nvidia_gpu()
gpu, vram = info if info else (None, 0)
if platform.system() == "Darwin":
    print("Mac detected -> default PyTorch (uses Apple GPU if available, else CPU)")
    pip("install", "torch")
elif gpu:
    new = any(k in gpu for k in ("RTX 50", "RTX PRO", "B200", "B100"))
    tag = "cu128" if new else "cu126"
    print(f"NVIDIA GPU found ({gpu}) -> PyTorch {tag}")
    pip("install", "torch", "--index-url", f"https://download.pytorch.org/whl/{tag}")
else:
    print("No NVIDIA GPU found -> CPU-only PyTorch")
    pip("install", "torch", "--index-url", "https://download.pytorch.org/whl/cpu")

pip("install", "-r", "requirements.txt")

import torch  # noqa: E402
print("\nInstalled torch", torch.__version__, "| CUDA available:", torch.cuda.is_available())
if platform.system() != "Darwin" and (not gpu or vram < 6000):
    print("\nTip: this machine has no GPU or under 6 GB VRAM. In .env set:")
    print("  RERANK_DEVICE=cpu")
    print("  CANDIDATES_PER_METHOD=10   (the reranker is slow on CPU, so keep the pool small)")
print("Next: copy .env.example to .env, add your OpenAI key, then follow the README.")
