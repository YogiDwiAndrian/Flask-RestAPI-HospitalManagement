import enum

class Gender(enum.Enum):
    MALE='MALE'
    FEMALE='FEMALE'

class Status(enum.Enum):
    IN_QUEUE='IN_QUEUE'
    DONE='DONE'
    CANCELLED='CANCELLED'