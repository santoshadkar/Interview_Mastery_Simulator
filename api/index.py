import sys
import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Add root directory to python module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domain.scenario_repository import ScenarioRepository
from src.domain.evaluation_engine import EvaluationEngine
from src.domain.statistics_tracker import StatisticsTracker

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "scenarios")
repository = ScenarioRepository(DATA_DIR)
stats_tracker = StatisticsTracker(repository)

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path == "/" or path == "/index.html" or path == "":
            ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "ui", "index.html")
            with open(ui_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/v1/health":
            body = json.dumps({"status": "online", "total_roles": 8, "version": "1.0.0"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/v1/roles":
            body = json.dumps(repository.get_roles()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/v1/stats":
            body = json.dumps(stats_tracker.get_summary_stats()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/v1/scenarios":
            role_id = query_params.get("role", [None])[0]
            difficulty = query_params.get("difficulty", [None])[0]
            limit = int(query_params.get("limit", [20])[0])
            offset = int(query_params.get("offset", [0])[0])

            if role_id:
                scenarios = repository.get_scenarios_for_role(role_id, target_count=100)
            else:
                scenarios = []
                for r in repository.get_roles():
                    scenarios.extend(repository.get_scenarios_for_role(r["id"], target_count=100))

            if difficulty:
                scenarios = [s for s in scenarios if difficulty.lower() in s["difficulty"].lower()]

            paginated = scenarios[offset:offset + limit]
            body = json.dumps({
                "total": len(scenarios),
                "limit": limit,
                "offset": offset,
                "scenarios": paginated
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path.startswith("/api/v1/scenarios/"):
            scenario_id = path.replace("/api/v1/scenarios/", "")
            scenario = repository.get_scenario_by_id(scenario_id)
            if scenario:
                body = json.dumps(scenario).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
            else:
                body = json.dumps({"error": f"Scenario '{scenario_id}' not found"}).encode("utf-8")
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/v1/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode("utf-8"))
                scenario_id = payload.get("scenario_id")
                user_response = payload.get("user_response", "")

                scenario = repository.get_scenario_by_id(scenario_id)
                if not scenario:
                    body = json.dumps({"error": f"Scenario '{scenario_id}' not found"}).encode("utf-8")
                    self.send_response(404)
                else:
                    eval_result = EvaluationEngine.evaluate(scenario, user_response)
                    body = json.dumps(eval_result).encode("utf-8")
                    self.send_response(200)
                
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                body = json.dumps({"error": f"Invalid evaluation request: {str(e)}"}).encode("utf-8")
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()
