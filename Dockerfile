FROM python:3.12-slim

# Evita criação de .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema para psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte
COPY . .

# Porta padrão do Koyeb
EXPOSE 8000

# Koyeb faz health check na porta 8000
# Usar uvicorn sem --reload em produção
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
