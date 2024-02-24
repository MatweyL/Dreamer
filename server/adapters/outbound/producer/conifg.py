from typing import Optional

from pydantic_settings import SettingsConfigDict, BaseSettings


class RabbitProducerConfig(BaseSettings):
    protocol: str = "amqp"
    user: str
    password: str
    host: str
    exchange_name: str
    exchange_type: str
    port: Optional[int]
    virtual_host: str = "/"
    reconnect_timeout_s: int
    produce_max_retries: int

    model_config = SettingsConfigDict(env_prefix='rabbit_consumer_')


rabbit_producer_config = RabbitProducerConfig()
