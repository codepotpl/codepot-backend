from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.models import Workshop


@api_view(['GET', ])
@permission_classes((AllowAny,))
def get_workshops(request, **kwargs):
    workshops = Workshop.objects.all()

    return Response(
        {
            'workshops': [
                {
                    'id': w.id,
                    'title': w.title,
                    'description': w.description,
                    'timeSlots': [
                        {
                            'id': ts.id,
                            'day': ts.timeslot_tier.day,
                            'startTime': ts.timeslot_tier.date_from.isoformat(),
                            'endTime': ts.timeslot_tier.date_to.isoformat(),
                            'room': ts.room_no,
                        } for ts in w.timeslot_set.all()
                        ],
                    'mentors': [
                        {
                            'id': m.id,
                            'firstName': m.first_name,
                            'lastName': m.last_name,
                        } for m in w.mentors.all()
                        ],
                    'tags': [
                      {
                        'id': t.name,
                            'name': t.name,
                      } for t in w.tags.all()
                      ],
                } for w in workshops
                ]
        },
        HTTP_200_OK
    )
