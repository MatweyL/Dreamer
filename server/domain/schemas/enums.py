import enum


class TaskStatus(str, enum.Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    IN_WORK = "IN_WORK"
    FINISHED = "FINISHED"
    ERROR = "ERROR"
