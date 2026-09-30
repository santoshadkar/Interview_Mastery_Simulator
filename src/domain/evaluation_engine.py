import re
from typing import Dict, Any, List

class EvaluationEngine:
    """
    Evaluates candidate responses against scenario rubrics and STAR principles.
    """
    
    @staticmethod
    def evaluate(scenario: Dict[str, Any], user_response: str) -> Dict[str, Any]:
        text_lower = user_response.lower()
        rubric = scenario.get("eval_rubric", {})
        key_competencies = rubric.get("key_competencies", [])
        must_include = rubric.get("must_include", [])
        common_pitfalls = rubric.get("common_pitfalls", [])
        
        # 1. STAR Alignment Detection
        star_alignment = {
            "situation_covered": any(k in text_lower for k in ["situation", "context", "background", "company", "firm", "project", "when", "faced"]),
            "task_covered": any(k in text_lower for k in ["task", "objective", "goal", "challenge", "responsibility", "needed to", "had to"]),
            "action_covered": any(k in text_lower for k in ["action", "did", "facilitated", "architected", "coached", "implemented", "introduced", "organized", "designed", "created"]),
            "result_covered": any(k in text_lower for k in ["result", "outcome", "metric", "improved", "dropped", "increased", "decreased", "%", "percent", "saved", "achieved"])
        }
        
        star_score = sum(1 for v in star_alignment.values() if v) * 15  # max 60 pts
        
        # 2. Competency Match
        matched_competencies = []
        for comp in key_competencies:
            keywords = comp.lower().split()
            if any(kw in text_lower for kw in keywords if len(kw) > 3):
                matched_competencies.append(comp)
        
        comp_score = (len(matched_competencies) / max(len(key_competencies), 1)) * 20  # max 20 pts
        
        # 3. Must-Include Points Match
        matched_must_include = []
        missed_must_include = []
        for point in must_include:
            words = [w for w in re.sub(r'[^\w\s]', '', point.lower()).split() if len(w) > 4]
            if any(w in text_lower for w in words):
                matched_must_include.append(point)
            else:
                missed_must_include.append(point)
                
        must_include_score = (len(matched_must_include) / max(len(must_include), 1)) * 20  # max 20 pts
        
        # 4. Pitfall Penalty Check
        detected_pitfalls = []
        for pitfall in common_pitfalls:
            p_words = [w for w in re.sub(r'[^\w\s]', '', pitfall.lower()).split() if len(w) > 4]
            if sum(1 for w in p_words if w in text_lower) >= 2:
                detected_pitfalls.append(pitfall)
                
        pitfall_penalty = len(detected_pitfalls) * 10
        
        # Total Overall Score
        total_score = max(0, min(100, int(star_score + comp_score + must_include_score - pitfall_penalty)))
        
        # Recommendations
        recommendations = []
        if not star_alignment["result_covered"]:
            recommendations.append("Include explicit quantitative metrics or outcomes in your 'Result' section.")
        if not star_alignment["action_covered"]:
            recommendations.append("Elaborate on your specific personal leadership actions rather than generic team efforts.")
        if missed_must_include:
            recommendations.append(f"Consider addressing critical key concepts: '{missed_must_include[0]}'")
        if detected_pitfalls:
            recommendations.append(f"Caution: Avoid common pitfall strategy: '{detected_pitfalls[0]}'")
            
        if not recommendations:
            recommendations.append("Outstanding response! Fully structured using STAR and hits all domain rubrics.")

        feedback_summary = (
            f"Candidate response scored {total_score}% readiness. "
            f"STAR coverage: {sum(1 for v in star_alignment.values() if v)}/4 components. "
            f"Matched {len(matched_must_include)} of {len(must_include)} essential rubric criteria."
        )
        
        return {
            "scenario_id": scenario.get("id"),
            "overall_score": total_score,
            "star_alignment": star_alignment,
            "competencies_matched": matched_competencies,
            "key_points_matched": matched_must_include,
            "missed_key_points": missed_must_include,
            "detected_pitfalls": detected_pitfalls,
            "feedback_summary": feedback_summary,
            "recommendations": recommendations,
            "hints": scenario.get("hints", []),
            "alternative_solutions": scenario.get("alternative_solutions", []),
            "star_model_answer": scenario.get("star_model_answer", {})
        }
