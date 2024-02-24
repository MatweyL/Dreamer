from pydantic_settings import SettingsConfigDict

from server.common.settings import SettingsElement


class Settings(SettingsElement):
    model_config = SettingsConfigDict(env_prefix="postgres_")

    user: str
    password: str
    host: str
    port: int
    db_name: str

    def get_db_url(self, async_mode=True):
        async_prefix = "+asyncpg" if async_mode else ""
        url_string = "postgresql{}://{}:{}@{}:{}/{}".format(async_prefix, self.user, self.password, self.host,
                                                            self.port, self.db_name)

        return url_string


settings = Settings()
