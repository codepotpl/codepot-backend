from codepot.exceptions import CodepotException


class WorkshopException(CodepotException):
    pass


class IllegalWorkshopAttendee(WorkshopException):
    def __init__(self, detail):
        super().__init__(detail, 500)
