from huggingface_hub import hf_hub_download

repo_id = "meta-llama/Llama-2-7b-chat-hf"
filename = "llama-2-7b.gguf"

path = hf_hub_download(repo_id, filename=filename, cache_dir="models")
print(f"Downloaded GGUF to {path}")
