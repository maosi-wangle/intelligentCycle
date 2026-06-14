from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.ai import AiAnswerData, AiSource
from app.services.deepseek_service import chat_completion
from app.services.memory_service import conversation_memory
from app.services.retrieval_service import get_question_context, retrieve_context


SYSTEM_PROMPT = Path(settings.ai_persona_path).read_text(encoding='utf-8')


def _build_messages(user_prompt: str, conversation_id: str | None = None) -> list[dict]:
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    if conversation_id:
        history = conversation_memory.history(conversation_id)
        for turn in history:
            messages.append({'role': turn.role, 'content': turn.content})
    messages.append({'role': 'user', 'content': user_prompt})
    return messages


def _store_turn(conversation_id: str | None, role: str, content: str) -> None:
    if conversation_id:
        conversation_memory.append(conversation_id, role, content)


def ask_with_agent(db: Session, question: str, use_retrieval: bool, conversation_id: str | None = None) -> AiAnswerData:
    context = ''
    sources: list[AiSource] = []
    if use_retrieval:
        context, sources = retrieve_context(db, question)

    user_prompt = 'User Question:\n' + question + '\n\n'
    if context:
        user_prompt += 'Retrieved Community Context:\n' + context + '\n\nUse the context when helpful and mention practical steps.'
    else:
        user_prompt += 'No relevant community context was found. Provide a concise helpful answer.'

    messages = _build_messages(user_prompt, conversation_id)
    answer = chat_completion(messages)
    _store_turn(conversation_id, 'user', question)
    _store_turn(conversation_id, 'assistant', answer)
    return AiAnswerData(answer=answer, sources=sources, conversation_id=conversation_id)


def draft_answer_for_question(db: Session, question_id: int, conversation_id: str | None = None) -> AiAnswerData:
    try:
        context, sources = get_question_context(db, question_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    user_prompt = (
        'Please draft a helpful community answer for the following question. '
        'Keep it practical, structured, and aligned with the existing answers when relevant.\n\n'
        + context
    )
    messages = _build_messages(user_prompt, conversation_id)
    answer = chat_completion(messages)
    _store_turn(conversation_id, 'user', f'question_id={question_id}')
    _store_turn(conversation_id, 'assistant', answer)
    return AiAnswerData(answer=answer, sources=sources, conversation_id=conversation_id)
