from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # Database (Supabase provides PostgreSQL connection string)
    database_url: str = ""  # Set a default value

    # JWT - Using Supabase JWT secret for RLS compatibility
    jwt_secret_key: str = "7shh8J7e4Q/MSbxZqDe5aaP3aEPuUUymdZjSD0KxJjyQ8A7KXEeIv4TrI0RhqWS1BnVncY4z5npwmA0sWCiENQ=="
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 10080  # 7 days

    # App
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
