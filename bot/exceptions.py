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


class FloodingDetectedException(Exception):

    def __init__(self, message: str, offender):
        super().__init__(message)
        self.offender = offender

    def log_transgression(self):
        log.warning(f"Transaction flooding @{self.offender.username} detected")
