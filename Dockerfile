FROM python:3.11-slim

# Diretório do aplicativo
WORKDIR /app

# Instala as dependências de sistema para o Chromium (necessário para o Kaleido)
RUN apt-get update && apt-get install -y --no-install-recommends chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código para dentro do contêiner
COPY . .

# Expõe a porta 5000 para o Gunicorn
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]