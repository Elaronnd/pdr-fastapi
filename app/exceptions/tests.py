class TestsError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TestError(TestsError):
    def __init__(self, test_id: int, message: str, status_code: int):
        self.test_id = test_id
        super().__init__(message=message, status_code=status_code)
