import asyncio
import json
from typing import Optional

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractExchange, AbstractConnection

from server.domain.schemas.full import FullPipelineStep
from server.ports.outbound import QueueProducerInterface
from server.ports.outbound.main import PipelineStepProducerI
from .utils import _build_connection_url

try:
    from server.common.logs import logger
except ImportError:
    import logging

    logger = logging
    logger.warning('failed to import project logger; use default logging')


class RabbitProducer(QueueProducerInterface):

    def __init__(self, protocol: str, user: str, password: str, host: str, port: str, virtual_host: str,
                 exchange_name: str, exchange_type: str,
                 reconnect_timeout_s: int,
                 produce_max_retries: int):
        self._connection_url = _build_connection_url(protocol, user, password, host, port, virtual_host)
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type

        self._reconnect_timeout_s = reconnect_timeout_s
        self._produce_max_retries = produce_max_retries

        self._connection: Optional[AbstractConnection] = None
        self._exchange: Optional[AbstractExchange] = None

    async def start(self):
        try:
            self._connection = await connect_robust(self._connection_url)
        except BaseException as e:
            logger.warning(f'{self} cannot create connection: {e}; sleep {self._reconnect_timeout_s} s and retry')
            await asyncio.sleep(self._reconnect_timeout_s)
            return await self.start()
        else:
            channel = await self._connection.channel()
            self._exchange = await channel.declare_exchange(self._exchange_name, self._exchange_type, durable=True)
            logger.info(f'{self} started')

    async def stop(self):
        if not self._connection.is_closed:
            await self._connection.close()
        logger.info(f'{self} stopped')

    async def produce(self, body: bytes, correlation_id: str, routing_key: str):
        current_retry = 0
        while current_retry < self._produce_max_retries:
            try:
                await self._exchange.publish(Message(body=body,
                                                     correlation_id=correlation_id, ),
                                             routing_key=routing_key)
            except BaseException as e:
                logger.error(f'{self} retry: [{current_retry}|{self._produce_max_retries}]; '
                             f'got exception while data producing: {e}')
                logger.exception(e)
                current_retry += 1
            else:
                logger.debug(f'{self} successfully produced task to {routing_key}')
                break


class RMQPipelineStepProducer(PipelineStepProducerI):

    def __init__(self, rabbit_producer: RabbitProducer):
        self._rabbit_producer = rabbit_producer

    async def produce(self, full_pipeline_step: FullPipelineStep):
        task = full_pipeline_step.current_task
        if full_pipeline_step.previous_task:
            for task_data in full_pipeline_step.previous_task.data_output:
                task.data_input.append(task_data)
        encoded_task: bytes = json.dumps(task.model_dump(), default=str, indent=2)
        await self._rabbit_producer.produce(encoded_task, None, task.type.name)
