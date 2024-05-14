from pydantic import ConfigDict
from pydantic_settings import SettingsConfigDict

from server.common.settings import SettingsElement


class DomainSettings(SettingsElement):
    model_config = SettingsConfigDict(env_prefix='domain_')
