FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install git+https://github.com/myshell-ai/MeloTTS.git && python -m unidic download
RUN pip install nltk

RUN python -m nltk.downloader averaged_perceptron_tagger_eng
# Copy the app code
COPY app/ .

EXPOSE 8000
CMD ["python", "server.py"]