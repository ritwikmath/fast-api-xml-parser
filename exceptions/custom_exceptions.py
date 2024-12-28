class CustomException(Exception):
    def __init__(self, status: int, message: str):
        self.status_code = status
        self.message = {"message": message}