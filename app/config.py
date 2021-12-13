from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str #="localhost"
    database_port: str #="5432"
    database_password: str #= "welcome1"
    database_name: str #= "fastapidb"
    database_username: str #= "postgres"
    secret_key : str #= "0123456789abcdefgh0987654321"
    algorithm : str #= "HS256"
    access_token_expire_minutes: int #= 30

    class Config: 
        env_file = ".env" #"C:\\dev\\restapi\\venv\\.env"

settings = Settings()
