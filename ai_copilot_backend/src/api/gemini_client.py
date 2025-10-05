from typing import List, Dict, Any

import httpx

from src.api.schemas import HistoryItem, ChatMessageRole


API_BASE = "https://generativelanguage.googleapis.com/v1beta"


def _to_gemini_parts(text: str) -> List[Dict[str, str]]:
    """Convert a text string into Gemini parts structure."""
    return [{"text": text}]


def _history_to_contents(history: List[HistoryItem]) -> List[Dict[str, Any]]:
    """
    Convert our history to Gemini 'contents' entries.
    Gemini expects a list of contents, where each item has:
      - role: "user" or "model"
      - parts: [{ "text": "..."}]
    We map:
      - user -> role "user"
      - assistant -> role "model"
    """
    contents: List[Dict[str, Any]] = []
    for item in history:
        role = "user" if item.role == ChatMessageRole.user else "model"
        contents.append({"role": role, "parts": _to_gemini_parts(item.content)})
    return contents


# PUBLIC_INTERFACE
async def generate_reply(message: str, history: List[HistoryItem], api_key: str, model: str) -> str:
    """
    Generate a reply from the Gemini API.

    Parameters:
    - message: Latest user message.
    - history: List of prior HistoryItem for context.
    - api_key: Google Generative Language API key.
    - model: Model name, e.g., "gemini-1.5-flash".

    Returns:
    - The assistant's reply text.

    Raises:
    - ValueError: If inputs are invalid or response parsing fails.
    - httpx.HTTPError: For HTTP transport errors.
    """
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")

    if not api_key or not api_key.strip():
        raise ValueError("API key is required.")

    if not model or not model.strip():
        raise ValueError("Model is required.")

    url = f"{API_BASE}/models/{model}:generateContent"
    params = {"key": api_key}

    # Build contents: prior turns + current user message
    contents = _history_to_contents(history)
    contents.append({"role": "user", "parts": _to_gemini_parts(message)})

    payload = {
        "contents": contents
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, params=params, json=payload)
        resp.raise_for_status()
        data = resp.json()

    # Expected structure:
    # {
    #   "candidates": [
    #     {
    #       "content": {
    #         "parts": [{"text": "..."}],
    #         ...
    #       },
    #       ...
    #     }
    #   ],
    #   ...
    # }
    try:
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("No candidates in Gemini response.")

        first = candidates[0]
        content = first.get("content") or {}
        parts = content.get("parts") or []

        # Concatenate all text parts in the first candidate
        texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        reply_text = " ".join(t.strip() for t in texts if t and t.strip())

        if not reply_text:
            raise ValueError("Empty reply received from Gemini.")

        return reply_text
    except (KeyError, TypeError, AttributeError) as e:
        raise ValueError("Failed to parse Gemini response.") from e
