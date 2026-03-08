import subprocess
import sys

print("Installing dependencies from requirements.txt...")

# Install everything
result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if result.returncode == 0:
    print("\n✅ All dependencies installed successfully!")
    print("\nTo run the API:")
    print("python -m app.main")
    print("\nOr:")
    print("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
else:
    print("\n❌ Installation failed. Trying individual packages...")
    
    # Try installing packages one by one
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "pyodbc==5.0.1",
        "alembic==1.12.1",
        "openai==1.6.1",
        "langchain==0.0.340",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "pydantic==2.5.3",
        "python-dotenv==1.0.0",
        "httpx==0.25.1",
        "requests==2.31.0",
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package])