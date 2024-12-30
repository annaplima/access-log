# Usar a imagem base com Apache Spark
FROM bitnami/spark:latest

# Garantir que estamos como root para rodar comandos de instalação
USER root

# Instalar Python e dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y python3 python3-pip

# Copiar o arquivo requirements.txt para o container
COPY requirements.txt .

# Atualizar o pip
RUN python3 -m pip install --upgrade pip

# Instalar as dependências
RUN pip3 install --no-cache-dir -r requirements.txt

# Configurações do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Criando o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do projeto para o container
COPY . /app

# Copiar a pasta src explicitamente para o container
COPY ./src /app/src

# Rodar o script Python (no diretório src)
CMD ["python3", "/app/run_all.py"]


