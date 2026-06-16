import httpx
import logging
from fastapi import HTTPException, status

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_api_key() -> str:
    api_key = settings.llm_api_key.strip()
    if not api_key:
        if settings.llm_base_url and ("localhost" in settings.llm_base_url or "127.0.0.1" in settings.llm_base_url):
            return "sk-local"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='LLM API key is not configured',
        )
    return api_key


def chat_completion(messages: list[dict]) -> str:
    if settings.llm_mock_mode:
        logger.info("LLM mock mode enabled, returning mock response")
        return "这是一个模拟的AI回复。由于网络限制，无法连接到真实的LLM API。你可以检查网络设置，或者配置代理来访问外部API。"
    
    api_key = ensure_api_key()
    base_url = settings.llm_base_url or "https://api.zhipuai.cn/v4/chat/completions"
    
    payload = {
        'model': settings.llm_model,
        'messages': messages,
        'temperature': 0.3,
    }
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    logger.info(f"Calling LLM API: model={settings.llm_model}, url={base_url}")
    logger.info(f"Payload size: {len(str(payload))} characters")
    
    client_kwargs = {'timeout': 120.0}
    if settings.http_proxy or settings.https_proxy:
        proxies = {}
        if settings.http_proxy:
            proxies['http://'] = settings.http_proxy
        if settings.https_proxy:
            proxies['https://'] = settings.https_proxy
        client_kwargs['proxies'] = proxies
        logger.info(f"Using proxy: {proxies}")
    
    try:
        with httpx.Client(**client_kwargs) as client:
            response = client.post(
                f'{base_url}', 
                headers=headers, 
                json=payload
            )
            logger.info(f"LLM API response status: {response.status_code}")
            logger.info(f"LLM API response headers: {dict(response.headers) if response.headers else 'None'}")
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text if exc.response is not None else 'LLM request failed'
        logger.error(f"LLM HTTP error: {exc.response.status_code if exc.response else 'unknown'} - {detail}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail) from exc
    except httpx.HTTPError as exc:
        logger.error(f"LLM connection error: {type(exc).__name__} - {str(exc)}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f'Unable to reach LLM API: {str(exc)}') from exc

    data = response.json()
    logger.info(f"LLM API response data keys: {list(data.keys())}")
    
    choices = data.get('choices') or []
    if not choices:
        logger.error(f"LLM returned no choices: {data}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='LLM returned no choices')

    message = choices[0].get('message') or {}
    content = message.get('content')
    if not content:
        logger.error(f"LLM returned empty content: {data}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='LLM returned empty content')
    return content.strip()