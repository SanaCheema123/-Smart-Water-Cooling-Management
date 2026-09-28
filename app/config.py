from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/water_cooling"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    weather_api_key: str = ""
    weather_lat: float = 31.4504
    weather_lon: float = 73.1350
    model_dir: str = "models"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
