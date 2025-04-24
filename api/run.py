import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

def main():
    """Run the API server."""
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 6996)),
        reload=True  # Enable auto-reload during development
    )

if __name__ == "__main__":
    main() 