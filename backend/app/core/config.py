from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "智答圈 API"
    app_env: str = "development"
    api_prefix: str = "/api"
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-v4-flash"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

