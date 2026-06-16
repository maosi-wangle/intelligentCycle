from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Intelligent Circle API'
    app_env: str = 'development'
    api_prefix: str = '/api'
    database_url: str = 'sqlite:///./app.db'
    jwt_secret_key: str = 'change-me-in-production'
    jwt_algorithm: str = 'HS256'
    jwt_expire_minutes: int = 60 * 24
    deepseek_api_key: str = ''
    deepseek_model: str = 'deepseek-v4-flash'
    llm_api_key: str = ''
    llm_base_url: str = 'https://api.zhipuai.cn/v4/chat/completions'
    llm_model: str = 'glm-4-7b-flash'
    ai_memory_window: int = Field(default=8, ge=2, le=20)
    ai_persona_path: str = 'agent/persona.md'
    cors_origins: list[str] = ['http://localhost:5173', 'http://127.0.0.1:5173']
    http_proxy: str = ''
    https_proxy: str = ''
    llm_mock_mode: bool = False

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return value

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()