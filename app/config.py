from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mfa_demo_code: str = "123456"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()