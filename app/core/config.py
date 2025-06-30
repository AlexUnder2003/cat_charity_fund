from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: EmailStr = "nW3yG@example.com"
    first_superuser_password: str = "pass"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
