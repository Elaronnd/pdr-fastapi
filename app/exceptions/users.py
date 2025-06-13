class UserError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UserIdError(UserError):
    def __init__(self, user_id: int, message: str, status_code: int):
        self.user_id = user_id
        super().__init__(message=message, status_code=status_code)


class UsernameError(UserError):
    def __init__(self, username: str, message: str, status_code: int):
        self.username = username
        super().__init__(message=message, status_code=status_code)
