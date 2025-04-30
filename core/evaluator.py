import yaml
import re
from pathlib import Path


class DynamicEvaluator:
    def __init__(self, profile="sales"):
        self.profile = self._load_profile(profile)

    def _load_profile(self, name):
        path = Path("config/scoring_profiles.yaml")
        with open(path) as f:
            profiles = yaml.safe_load(f)
        return profiles.get(name, {})

    def evaluate(self, prompt, response):
        scores = {}
        total_weight = 0

        for criterion in self.profile.get("criteria", []):
            # CTA Detection
            if "regex" in criterion:
                count = len(re.findall(criterion["regex"], response.lower()))
                score = min(criterion["max_score"], count)

            # Word Count Scoring
            elif criterion.get("scoring") == "word_count":
                words = len(response.split())
                for threshold in criterion["thresholds"]:
                    if threshold["min"] <= words <= threshold["max"]:
                        score = threshold["score"]
                        break

            # Phrase Requirements
            elif "required_phrases" in criterion:
                score = all(phrase in response for phrase in criterion["required_phrases"])
                score = criterion["max_score"] if score else 0

            scores[criterion["name"]] = {
                "score": score,
                "weight": criterion["weight"]
            }
            total_weight += criterion["weight"]

        # Calculate weighted total
        overall = sum(
            v["score"] * v["weight"]
            for v in scores.values()
        ) / total_weight

        return {
            "overall": round(overall, 1),
            "criteria": scores
        }