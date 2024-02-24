from server.ports.outbound import QueueProducerInterface


class RabbitProducerMock(QueueProducerInterface):

    async def start(self):
        pass

    async def stop(self):
        pass

    async def produce(self, body: bytes, correlation_id: str, routing_key: str):
        pass
