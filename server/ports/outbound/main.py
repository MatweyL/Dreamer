from abc import ABC, abstractmethod

from server.domain.schemas.full import FullPipelineStep


class PipelineStepProducerI(ABC):
    @abstractmethod
    async def produce(self, full_pipeline_step: FullPipelineStep):
        pass
