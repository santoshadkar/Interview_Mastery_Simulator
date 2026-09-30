import sys
import os

# Add root directory to python module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.server import ScenarioAPIHandler

# Vercel python serverless handler entrypoint
handler = ScenarioAPIHandler
