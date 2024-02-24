from server.adapters.outbound.repository.orm_sqlalchemy import models
from server.adapters.outbound.repository.orm_sqlalchemy.abstract import AbstractSQLAlchemyRepository
from server.domain import schemas
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineRepository


class PipelineSQLAlchemyRepository(AbstractPipelineRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.Pipeline) -> schemas.Pipeline:
        return schemas.Pipeline(
            uid=obj.uid,
            name=obj.name
        )

    def entity_model(self, obj: schemas.Pipeline) -> models.Pipeline:
        return models.Pipeline(
            uid=obj.uid, name=obj.name
        )
