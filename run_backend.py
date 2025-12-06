import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get port and host from environment variables, with defaults
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8001"))
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")

if __name__ == "__main__":
    print(f"🚀 Starting backend server on {BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run("main:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=True)

