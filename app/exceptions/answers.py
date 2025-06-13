class AnswerError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class AnswerImageError(AnswerError):
    def __init__(self, filename: str, message: str, status_code: int):
        self.filename = filename
        super().__init__(message=message, status_code=status_code)

class AnswerIdError(AnswerError):
    def __init__(self, answer_id: int, message: str, status_code: int):
        self.answer_id = answer_id
        super().__init__(message=message, status_code=status_code)
