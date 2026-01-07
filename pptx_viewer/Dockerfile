FROM python:3.11-slim

# Install libreoffice for pptx -> png conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-impress \
    libreoffice-core \
    libreoffice-common \
    poppler-utils \
    fonts-dejavu-core \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh

ENV FLASK_ENV=production
EXPOSE 5000
ENTRYPOINT ["/app/entrypoint.sh"]
