class SourceFileError(Exception):
    """Custom error to indicate when chosen file does not contain data that would support a function call.

    For example, selecting 'countries' when calling extract_diplomats()
    """

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)
