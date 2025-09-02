import json
import random
from typing import List, Dict

PROMPT_SUPERPOSITIONS = [
    {
        "title": "Cold Email Quantum",
        "body": "Reach out with entangled value propositions and superposed greetings."
    },
    {
        "title": "Landing Page Quantum",
        "body": "Present your product in a state of maximum uncertainty and appeal."
    },
    {
        "title": "Competitor Analysis Quantum",
        "body": "Analyze rivals with non-local insights and quantum feedback."
    }
]

def generate_superposed_prompts(n: int = 3) -> List[Dict]:
    """Generate n quantum superposed prompts."""
    return random.sample(PROMPT_SUPERPOSITIONS, min(n, len(PROMPT_SUPERPOSITIONS)))

def entangle_prompts(prompts: List[Dict]) -> Dict:
    """Entangle prompts so that changing one element affects all."""
    entangled = {}
    shared_title = random.choice([p["title"] for p in prompts])
    shared_body = " | ".join([p["body"] for p in prompts])
    entangled["title"] = shared_title + " (Entangled)"
    entangled["body"] = shared_body
    return entangled

def collapse_prompt(prompts: List[Dict]) -> Dict:
    """Collapse superposed prompts to a single prompt (measurement)."""
    return random.choice(prompts)


