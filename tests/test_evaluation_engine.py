import unittest
from src.domain.evaluation_engine import EvaluationEngine

class TestEvaluationEngine(unittest.TestCase):
    def setUp(self):
        self.scenario = {
            "id": "AIE-001",
            "eval_rubric": {
                "key_competencies": ["RAG Architecture", "Prompt Engineering"],
                "must_include": ["RAG Triad", "Semantic chunking", "Re-ranking"],
                "common_pitfalls": ["Increasing LLM temperature"]
            },
            "star_model_answer": {
                "situation": "High hallucination in enterprise RAG.",
                "task": "Fix grounding accuracy.",
                "action": "Applied RAG Triad, semantic chunking, prompt engineering, and re-ranking.",
                "result": "Groundedness reached 97.4%."
            }
        }

    def test_evaluation_high_score(self):
        good_response = (
            "Situation: In a recent enterprise project, RAG context relevance was dropping. "
            "Task: My task was to diagnose and fix groundedness using RAG Architecture and Prompt Engineering. "
            "Action: I implemented RAG Triad evaluation, changed chunking to semantic chunking, and added a cross-encoder re-ranking step. "
            "Result: Groundedness improved to 97% and customer support tickets dropped by 40%."
        )
        result = EvaluationEngine.evaluate(self.scenario, good_response)
        self.assertGreaterEqual(result["overall_score"], 80)
        self.assertTrue(result["star_alignment"]["situation_covered"])
        self.assertTrue(result["star_alignment"]["result_covered"])

    def test_evaluation_detects_missed_points(self):
        vague_response = "I looked at the server logs and changed some code to make it run faster."
        result = EvaluationEngine.evaluate(self.scenario, vague_response)
        self.assertLess(result["overall_score"], 50)
        self.assertIn("RAG Triad", result["missed_key_points"])

if __name__ == "__main__":
    unittest.main()
