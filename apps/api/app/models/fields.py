from sqlalchemy import DateTime, TypeDecorator

class AwareDatetime(TypeDecorator):
    impl = DateTime

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if not value.tzinfo:
            raise TypeError("tzinfo is required")
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value, dialect):
        return value if value is None else value.replace(tzinfo=timezone.utc)
