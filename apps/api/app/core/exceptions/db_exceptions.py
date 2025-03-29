from sqlalchemy.exc import DatabaseError

from .color_agent_exception import ColorAgentException


class PostgreSQLError(ColorAgentException):
    def __init__(self, err: DatabaseError):
        super().__init__(err)
        self.exec = err
