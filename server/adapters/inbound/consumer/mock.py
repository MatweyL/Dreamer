from typing import Callable

from server.ports.inbound import QueueConsumerInterface


class RabbitConsumerMock(QueueConsumerInterface):

    async def start(self):
        pass

    async def stop(self):
        pass

    async def consume_queue(self, queue_name: str, processing_callback: Callable):
        pass
