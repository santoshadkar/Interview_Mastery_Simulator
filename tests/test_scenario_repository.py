import unittest
import os
from src.domain.scenario_repository import ScenarioRepository, ROLES

class TestScenarioRepository(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "scenarios")
        self.repo = ScenarioRepository(self.data_dir)

    def test_roles_count(self):
        roles = self.repo.get_roles()
        self.assertEqual(len(roles), 8, "Should support exactly 8 roles across Agile and AI tracks")

    def test_target_100_scenarios_per_role(self):
        for role in ROLES:
            scenarios = self.repo.get_scenarios_for_role(role["id"], target_count=100)
            self.assertEqual(len(scenarios), 100, f"Role '{role['id']}' should have exactly 100 scenarios")

    def test_scenario_uniqueness_guarantee(self):
        """Verifies 100% uniqueness with zero duplicate IDs or titles across all 800 scenarios."""
        all_ids = set()
        all_titles = set()
        total_count = 0

        for role in ROLES:
            scenarios = self.repo.get_scenarios_for_role(role["id"], target_count=100)
            for s in scenarios:
                total_count += 1
                self.assertNotIn(s["id"], all_ids, f"Duplicate Scenario ID found: {s['id']}")
                self.assertNotIn(s["title"], all_titles, f"Duplicate Scenario Title found: {s['title']}")
                all_ids.add(s["id"])
                all_titles.add(s["title"])

        self.assertEqual(total_count, 800, "Should generate exactly 800 total unique scenarios")
        self.assertEqual(len(all_ids), 800, "All 800 Scenario IDs must be unique")
        self.assertEqual(len(all_titles), 800, "All 800 Scenario Titles must be unique")

    def test_get_scenario_by_id(self):
        scenario = self.repo.get_scenario_by_id("AC-001")
        self.assertIsNotNone(scenario, "Scenario AC-001 should be retrievable")
        self.assertEqual(scenario["role_id"], "agile_coach")
        self.assertIn("eval_rubric", scenario)

if __name__ == "__main__":
    unittest.main()
