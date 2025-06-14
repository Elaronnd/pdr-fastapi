class QuestionsError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class QuestionsListError(QuestionsError):
    def __init__(self, questions_id: list[int], message: str, status_code: int):
        self.questions_id = questions_id
        super().__init__(message=message, status_code=status_code)


class QuestionError(QuestionsError):
    def __init__(self, question_id: int, message: str, status_code: int):
        self.question_id = question_id
        super().__init__(message=message, status_code=status_code)


class QuestionImageError(QuestionsError):
    def __init__(self, filename: str, message: str, status_code: int):
        self.filename = filename
        super().__init__(message=message, status_code=status_code)
