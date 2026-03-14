from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 3000               
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int = 3306             

    model_config = SettingsConfigDict(
        env_file=".env",                
        env_file_encoding="utf-8",
        case_sensitive=False,           
        extra="ignore"                  
    )

settings = Settings()