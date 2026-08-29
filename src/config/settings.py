from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    top_k: int = 3
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://127.0.0.1:11434"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()