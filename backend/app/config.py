from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = 'Imp117qang'
    database_port:str = 'localhost'
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env"


settings = Settings()