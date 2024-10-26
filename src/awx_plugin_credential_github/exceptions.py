class MissingParameterError(ValueError):
    def __init__(self, parameter: str) -> None:
        super().__init__(f"The parameter(s) '{parameter.join(',')}' was not provided.")
