import os


def call_ai(prompt: str, kanban: dict):
    """Placeholder AI call. If OPENROUTER_API_KEY is set, this should be replaced
    with a real call to OpenRouter. For now we return an echo or an error message."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return {"error": "OPENROUTER_API_KEY not set; AI disabled for now", "echo": prompt}
    # TODO: Implement real OpenRouter call
    return {"response": f"Echo: {prompt}"}
