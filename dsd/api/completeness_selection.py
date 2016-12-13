from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.completeness_service import check_parameter, fetch_completeness_from_remote_database, \
    fetch_total_facility_from_remote_database, fetch_used_facility_from_remote_database, fetch_ou_name_by_ou_id

COMPLETED = 'completed'
INCOMPLETE = 'incomplete'
MISSING = 'missing'
TOTAL_FACILITY = 'total'
USED_FACILITY = 'used'


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def data_completeness_endpoint(request):
    try:
        year_num, week_num, ou = check_parameter(request.GET)

        ous = fetch_ou_name_by_ou_id(ou)

        total_facilities = fetch_total_facility_from_remote_database(ous)
        used_facilities = fetch_used_facility_from_remote_database(ous)
        completed, incomplete, _ = fetch_completeness_from_remote_database(year_num, week_num, ous)
        missing = used_facilities - completed - incomplete

        response = {
            'total': total_facilities,
            'mBes': [
                {'status': COMPLETED, 'amount': completed},
                {'status': INCOMPLETE, 'amount': incomplete},
                {'status': MISSING, 'amount': missing}
            ]
        }
        return Response(response, status=status.HTTP_200_OK)

    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)

    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
