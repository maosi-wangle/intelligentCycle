import httpx
from fastapi import HTTPException, status

from app.core.config import settings


DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'


def ensure_api_key() -> str:
    api_key = settings.deepseek_api_key.strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='DeepSeek API key is not configured',
        )
    return api_key


def chat_completion(messages: list[dict]) -> str:
    api_key = ensure_api_key()
    payload = {
        'model': settings.deepseek_model,
        'messages': messages,
        'temperature': 0.3,
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text if exc.response is not None else 'DeepSeek request failed'
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='Unable to reach DeepSeek API') from exc

    data = response.json()
    choices = data.get('choices') or []
    if not choices:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='DeepSeek returned no choices')

    message = choices[0].get('message') or {}
    content = message.get('content')
    if not content:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='DeepSeek returned empty content')
    return content.strip()
