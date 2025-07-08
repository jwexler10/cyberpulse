#!/usr/bin/env python3
"""
Convert the Meta-Llama 2 7B checkpoint to GGUF and store everything
on the external drive /Volumes/WEXLER to save internal-SSD space.
"""

import os
from subprocess import run, CalledProcessError
from transformers import AutoModelForCausalLM, AutoTokenizer

# ----  Paths on the external drive  ---------------------------------

EXT_ROOT   = "/Volumes/WEXLER"
TMP_DIR    = os.path.join(EXT_ROOT, "temp_llama")              # PyTorch checkpoint
OUT_DIR    = os.path.join(EXT_ROOT, "cyberpulse_models")       # final GGUF file
OUTPUT_PATH = os.path.join(OUT_DIR, "llama-2-7b.gguf")

os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ----  Download PyTorch weights + tokenizer  ------------------------

print("📥  Downloading PyTorch checkpoint to external drive…")
AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype="auto",
    cache_dir=TMP_DIR
).save_pretrained(TMP_DIR)

AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    cache_dir=TMP_DIR
).save_pretrained(TMP_DIR)

# ----  Convert to GGUF  ---------------------------------------------

print("🔄  Converting to GGUF (this can take ~30 min)…")
try:
    run([
        "convert-llama-to-gguf",
        "--model_path", TMP_DIR,
        "--outtype", "gguf",
        "--output_path", OUTPUT_PATH
    ], check=True)
    print(f"✅  GGUF written to {OUTPUT_PATH}")
except CalledProcessError as e:
    print("❌  Conversion failed:", e)
    exit(1)

# ----  Cleanup prompt (optional)  -----------------------------------

print("\nYou can now delete the temporary PyTorch checkpoint to free ~10 GB:")
print(f"  rm -rf {TMP_DIR}")
