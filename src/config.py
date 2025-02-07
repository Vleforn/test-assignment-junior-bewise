import dotenv
import os

dotenv.load_dotenv(".env")

class Settings:

    @property
    def postgres_url(self):
        username = self._get_env("POSTGRES_USERNAME")
        password = self._get_env("POSTGRES_PASSWORD")
        db_address = self._get_env("POSTGRES_DB_ADDRESS")
        db_name = self._get_env("POSTGRES_DB_NAME")
        return f"postgresql+asyncpg://{username}:{password}@{db_address}/{db_name}"

    @property
    def api_url(self):
        url = self._get_env("OPENTDB_API_URL")
        return url

    @property
    def token_url(self):
        url = self._get_env("OPENTDB_TOKEN_URL")
        return url

    @property
    def token(self):
        token = os.getenv("TOKEN")
        if token is None:
            self._update_token()
        token = self._get_env("TOKEN")
        return token

    def _update_token(self):
        pass
    
    def _get_env(self, var_name: str) -> str:
        var_val = os.getenv(var_name)
        if var_val is None:
            raise ValueError(f"Enviromental variable haven't found: {var_name}")
        return var_val

settings = Settings()
settings.token_url
