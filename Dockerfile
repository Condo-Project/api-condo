# Imagem base oficial do Python 3.10
FROM python:3.11.2-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do código da aplicação para o container
COPY . .

# Expõe a porta padrão do FastAPI (8000)
EXPOSE 8000
CMD python main.py
