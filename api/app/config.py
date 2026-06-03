from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    secret_key: str
    stripe_secret_key: str
    stripe_webhook_secret: str
    frontend_url: str = "http://localhost:4321"
    admin_email: str = "admin@rackside.app"
    admin_password: str = "rackside-admin"
    access_token_ttl_minutes: int = 480


settings = Settings()
