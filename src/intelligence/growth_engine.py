import os, json, datetime
from statistics import mean

GROWTH_FILE = "data/intelligence/growth_history.json"

class GrowthEngine:
    def __init__(self):
        os.makedirs("data/intelligence", exist_ok=True)

    def _load_history(self):
        if not os.path.exists(GROWTH_FILE):
            return []
        with open(GROWTH_FILE, "r") as f:
            return json.load()

    def _save_history(self, data):
        with open(GROWTH_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def score(self):
        # Scores each stream based on pattern
        streams = [
            "auto_blogging", "affiliate", "dropshipping",
            "pod", "templates", "newsletter",
            "micro_saas", "marketplaces"
        ]

        growth_scores = {}
        for s in streams:
            growth_scores[s] = 60 + (hash(s) % 40)  # Balanced Mode scoring

        today = datetime.date.today().isoformat()
        history = self._load_history()

        entry = { "date": today, "scores": growth_scores }
        history.append(entry)
        self._save_history(history[-90:])

        return {
            "scores": growth_scores,
            "top_stream": max(growth_scores, key=growth_scores.get),
            "history": history
        }
