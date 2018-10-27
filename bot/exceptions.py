class FoodProcessorError(Exception):
    pass


class ConnectionProblem(FoodProcessorError):
    pass


class ParsingError(FoodProcessorError):
    pass
