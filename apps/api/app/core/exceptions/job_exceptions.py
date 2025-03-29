from .color_agent_exception import ColorAgentException


class ExceptionInRunner(ColorAgentException):
    """
    Exception raised when an exception is raised in the executor.
    """

    def __init__(self):
        msg = "The runner thread which was running the jobs raised an exeception. Read the traceback above to debug it. You can also pass `raise_exceptions=False` incase you want to show only a warning message instead."
        super().__init__(msg)


class ScraperDidNotFinishException(ColorAgentException):
    """
    Exception raised when any of the vendor web scrapers did not finish.
    """

    def __init__(self):
        msg = "The scraping of latest product data was not completed."
        super().__init__(msg)
