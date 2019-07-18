import logging
log = logging.getLogger()


class FoodProcessorError(Exception):
    pass


class ConnectionProblem(FoodProcessorError):
    pass


class ParsingError(FoodProcessorError):
    pass


class TransactionError(Exception):
    pass


class TransactionArgsParsingError(TransactionError):
    pass


class TooPoorException(TransactionError):
    pass


class TooRichException(TransactionError):
    pass


class FloodingError(TransactionError):

    def __init__(self, message: str):
        super().__init__(message)
        self.offender = None

    def log_transgression(self, offender):
        self.offender = offender
        log.warning(f"Transaction flooding @{self.offender.username} detected")
