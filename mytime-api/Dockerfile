FROM python:3.11-slim

# 1. Install SQL Server ODBC Driver 18 (updated method)
RUN apt-get update && \
    apt-get install -y curl gnupg2 && \
    # Download Microsoft GPG key
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc -o /etc/apt/trusted.gpg.d/microsoft.gpg && \
    # Add Microsoft repository
    echo "deb [arch=amd64] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    # Install ODBC driver
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    # Install ODBC dev tools
    apt-get install -y unixodbc-dev && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Python packages
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy application code
COPY . .

# 4. Start the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
