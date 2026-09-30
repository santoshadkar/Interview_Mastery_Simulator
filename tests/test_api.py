import unittest
import json
import urllib.request
import urllib.parse
import threading
import time
from src.api.server import run_server

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8899
        cls.server_thread = threading.Thread(target=run_server, args=(cls.port,), daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Allow server to start

    def test_health_endpoint(self):
        url = f"http://localhost:{self.port}/api/v1/health"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "online")

    def test_roles_endpoint(self):
        url = f"http://localhost:{self.port}/api/v1/roles"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            roles = json.loads(response.read().decode("utf-8"))
            self.assertEqual(len(roles), 8)

    def test_scenarios_query_endpoint(self):
        url = f"http://localhost:{self.port}/api/v1/scenarios?role=ai_engineer&limit=5"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["total"], 100)
            self.assertEqual(len(data["scenarios"]), 5)

if __name__ == "__main__":
    unittest.main()
