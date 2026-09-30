import json
import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.domain.scenario_repository import ScenarioRepository
from src.domain.evaluation_engine import EvaluationEngine
from src.domain.statistics_tracker import StatisticsTracker

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "scenarios")
repository = ScenarioRepository(DATA_DIR)
stats_tracker = StatisticsTracker(repository)

class ScenarioAPIHandler(BaseHTTPRequestHandler):
    
    def _send_json(self, data: Any, status_code: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: str, content_type: str):
        if not os.path.exists(file_path):
            self.send_error(404, "File Not Found")
            return
        with open(file_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Serve Web Portal UI
        if path == "/" or path == "/index.html":
            ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "index.html")
            self._send_file(ui_path, "text/html; charset=utf-8")
            return

        # API Endpoints
        if path == "/api/v1/health":
            self._send_json({
                "status": "online",
                "total_roles": 8,
                "target_scenarios_per_role": 100,
                "version": "1.0.0"
            })
            return

        if path == "/api/v1/roles":
            roles = repository.get_roles()
            self._send_json(roles)
            return

        if path == "/api/v1/stats":
            stats = stats_tracker.get_summary_stats()
            self._send_json(stats)
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
            self._send_json({
                "total": len(scenarios),
                "limit": limit,
                "offset": offset,
                "scenarios": paginated
            })
            return

        if path.startswith("/api/v1/scenarios/"):
            scenario_id = path.replace("/api/v1/scenarios/", "")
            scenario = repository.get_scenario_by_id(scenario_id)
            if scenario:
                self._send_json(scenario)
            else:
                self._send_json({"error": f"Scenario '{scenario_id}' not found"}, status_code=404)
            return

        self.send_error(404, "Endpoint not found")

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
                    self._send_json({"error": f"Scenario '{scenario_id}' not found"}, status_code=404)
                    return

                eval_result = EvaluationEngine.evaluate(scenario, user_response)
                self._send_json(eval_result)
            except Exception as e:
                self._send_json({"error": f"Invalid evaluation request: {str(e)}"}, status_code=400)
            return

        self.send_error(404, "Endpoint not found")

def run_server(port: int = 8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ScenarioAPIHandler)
    print(f"Scenario Interview Simulation Portal running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
