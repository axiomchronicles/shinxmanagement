
class AccountRegistrationError(Exception):
    def __init__(self, details: str = "", code: int = 200, *args):
        self.details = details
        self.code = code
        super().__init__(*args)