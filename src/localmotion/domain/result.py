from src.localmotion.domain.playground import Playground


class Result:
    def __init__(self, playground: Playground, message=None, exception=None) -> None:
        self.playground = playground
        self.message = message
        self.exception = exception
        self.line_number = 0

    @classmethod
    def success(cls, playground: Playground, message: str) -> 'Result':
        return cls(playground=playground, message=message, exception=None)

    @classmethod
    def failure(cls, playground: Playground, message: str) -> 'Result':
        return cls(playground=playground, message=message, exception=None)

    @classmethod
    def exception(cls, playground: Playground, message: str, exception: BaseException) -> 'Result':
        return cls(playground=playground, message=message, exception=exception)

    @classmethod
    def general_failure(cls, playground: Playground, message: str) -> 'Result':
        return cls(playground=playground, message=message, exception=None)

    def assign_line_number(self, line_number: int):
        self.line_number = line_number

    def is_failure(self):
        return self.exception is not None
