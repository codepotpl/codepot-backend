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


class WorkshopMessageNotFoundException(WorkshopException):
  def __init__(self, workshop_id=None):
    super().__init__('Workshop message with ID: {} not found'.format(workshop_id), 503)


class WorkshopWithoutPurchaseSignAttemptException(WorkshopException):
  def __init__(self, user_id):
    super().__init__('User with ID: {} does not have valid purchase.'.format(user_id), 504)


class UserAlreadySignedForWorkshopException(WorkshopException):
  def __init__(self, user_id, workshop_id):
    super().__init__('User with ID: {} already signed for workshop with ID: {}.'.format(user_id, workshop_id), 505)

class MentorCannotSignForOwnWorkshopException(WorkshopException):
  def __init__(self, user_id, workshop_id):
    super().__init__('User with ID: {} is workshop with ID: {} mentor.'.format(user_id, workshop_id), 506)


class WorkshopMaxAttendeesLimitExceededException(WorkshopException):
  def __init__(self, workshop):
    super().__init__(
      'Max attendees limit ({}) reached for workshop with ID: {}.'.format(workshop.max_attendees, workshop.id), 507)


class UserAlreadySignedForWorkshopInTierException(WorkshopException):
  def __init__(self, detail):
    super().__init__(detail, 508)


class UserNotSignedForWorkshopException(WorkshopException):
  def __init__(self, user_id, workshop_id):
    super().__init__('User with ID: {} is not signed for workshop with ID: {}'.format(user_id, workshop_id), 509)


class MutuallyExclusiveTiersException(WorkshopException):
  def __init__(self):
    super().__init__('Cannot sign for workshop when tiers are mutually exclusive.', 510)


class WorkshopHasAlreadyStartedException(WorkshopException):
  def __init__(self, workshop_id):
    super().__init__('Workshop with ID: {} has already started.'.format(workshop_id), 511)
