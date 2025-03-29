from .color_agent_exception import ColorAgentException


class CacheIdentificationInferenceError(ColorAgentException):
    def __init__(self, message: str = "Could not infer id for resource being cached.") -> None:
        self.message = message
        super().__init__(self.message)


class CacheInvalidRequestError(ColorAgentException):
    def __init__(self, message: str = "Type of request not supported.") -> None:
        self.message = message
        super().__init__(self.message)


class CacheMissingClientError(ColorAgentException):
    def __init__(self, message: str = "Client is None.") -> None:
        self.message = message
        super().__init__(self.message)
