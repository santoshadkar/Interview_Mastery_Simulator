import sys
import os

# Add project root directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.server import run_server

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
