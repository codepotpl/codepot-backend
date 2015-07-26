from codepot.exceptions import CodepotException


class WorkshopException(CodepotException):
    pass


class IllegalWorkshopAttendee(WorkshopException):
    def __init__(self, detail):
        super().__init__(detail, 500)


class WorkshopNotFoundException(WorkshopException):
  def __init__(self, workshop_id=None):
    super().__init__('Workshop with ID: {} not found'.format(workshop_id), 501)


class WorkshopIllegalAccessException(WorkshopException):
  def __init__(self, detail):
    super().__init__(detail, 502)
