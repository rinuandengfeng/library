
from log import logger

class SeatException(Exception):

    def __init__(self, message) -> None:
        super().__init__(message)
        logger.error(message)