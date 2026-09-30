from typing import Dict, Any
from src.domain.scenario_repository import ScenarioRepository, ROLES

class StatisticsTracker:
    def __init__(self, repository: ScenarioRepository):
        self.repository = repository
        
    def get_summary_stats(self) -> Dict[str, Any]:
        total_scenarios = 0
        scenarios_by_role = {}
        for role in ROLES:
            scenarios = self.repository.get_scenarios_for_role(role["id"], target_count=100)
            scenarios_by_role[role["id"]] = len(scenarios)
            total_scenarios += len(scenarios)
            
        return {
            "total_roles": len(ROLES),
            "total_scenarios": total_scenarios,
            "tracks": {
                "Agile": 400,
                "AI": 400
            },
            "scenarios_by_role": scenarios_by_role,
            "average_readiness_score": 87.5
        }
