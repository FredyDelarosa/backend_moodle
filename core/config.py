from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str
    moodle_url: str = "http://localhost/moodle"
    moodle_token: str
    concurrency_limit: int = 5
    app_port: int = 8000

    # CORS settings (can be configured via environment variables)
    cors_allow_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()