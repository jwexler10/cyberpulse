# Dockerfile

# Use the official slim Python image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Install compilers, Python headers, CMake, and Git LFS (for GGUF support)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       cmake \
       python3-dev \
       git-lfs \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirement files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies (including llama-cpp-python)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ src/
COPY setup.py ./
COPY .gitignore ./

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Copy a blank config so login works in-container
RUN mkdir -p /root/.cyberpulse \
    && cp /app/src/cyberpulse/config.py /root/.cyberpulse/config.yml

# Entrypoint: default to showing help
ENTRYPOINT ["cyberpulse"]
CMD ["--help"]
