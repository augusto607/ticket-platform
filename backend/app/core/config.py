from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central settings object.

    BaseSettings reads values from environment variables automatically.
    That lets us keep config outside the code.
    """

    # Application settings
    app_name: str = "Ticket Platform API"
    app_env: str = "development"
    app_port: int = 8000

    # Database settings
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432

    # Security settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Tell Pydantic to read values from a .env file if available
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """
        Build the SQLAlchemy/PostgreSQL connection string dynamically.
        This avoids hardcoding it in multiple places.
        """
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Create a single reusable settings instance
settings = Settings()
