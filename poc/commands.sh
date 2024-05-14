# Fix "Failed to initialize NVML" error
# https://github.com/NVIDIA/nvidia-container-toolkit/issues/381#issuecomment-1986856849
# sudo vim /etc/nvidia-container-runtime/config.toml
# no-cgroups = false
# sudo systemctl restart docker
# sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi

# Run Voicevox Engine
docker run --rm -p '0.0.0.0:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --runtime=nvidia --rm --gpus all -p '0.0.0.0:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest

docker run --rm -p 3000:8080 --network=host -v open-webui:/app/backend/data -e OLLAMA_API_BASE_URL=http://127.0.0.1:11434/api --name open-webui ghcr.io/open-webui/open-webui:main
