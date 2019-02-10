import neocortex


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

    def __init__(self, message: str, offender: neocortex.User):
        super().__init__(message)
        self.offender = offender
