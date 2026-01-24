FROM python:3.11-slim

# 1. Install SQL Server ODBC Driver - UPDATED METHOD
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    # Download Microsoft GPG key and add it
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    # Add Microsoft repository with proper signing
    echo "deb [signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    # Install ODBC driver
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    # Install ODBC development files
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
