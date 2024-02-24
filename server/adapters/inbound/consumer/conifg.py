from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitConsumerConfig(BaseSettings):
    protocol: str = "amqp"
    user: str
    password: str
    host: str
    port: Optional[int]
    virtual_host: str = "/"
    reconnect_timeout_s: int

    model_config = SettingsConfigDict(env_prefix='rabbit_consumer_')


rabbit_consumer_config = RabbitConsumerConfig()
