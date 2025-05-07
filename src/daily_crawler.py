import time
import subprocess
import os
import sys
from datetime import datetime

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "crypto_history_scraper.py")

def run_script():
    print(f"Running: {SCRIPT_PATH} at {datetime.now()}")
    subprocess.run([sys.executable, SCRIPT_PATH])

if __name__ == "__main__":
    while True:
        run_script()
        print("Sleeping 24 hours...")
        time.sleep(24 * 3600)
