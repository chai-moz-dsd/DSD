from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import io

import xlsxwriter
from django.http import HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.submission_service import START_DAY, END_DAY, LOCATION, INDEX_PAGE, fetch_ou_id_by_ou_uid
from dsd.services.export_excel_service import create_excel


@csrf_exempt
@require_http_methods(['GET'])
def data_submission_excel_endpoint(request):
    try:
        start, end, ou, page_index = check_params(request.GET)
    except IllegalArgumentException as e:
        return HttpResponse(status=500, reason=e.error_message)

    location_level, location_id = fetch_ou_id_by_ou_uid(ou)
    start_day = datetime.fromtimestamp(float(start) / 1000).strftime('%Y-%m-%d')
    end_day = datetime.fromtimestamp(float(end) / 1000).strftime('%Y-%m-%d')

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Todas Submicoes')
    create_excel(workbook, worksheet, location_level, location_id, start_day, end_day)
    workbook.close()

    output.seek(0)
    response = FileResponse(output, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename={}".format(
        'TodasSubmicoes{}-{}.xlsx'.format(start_day, end_day))

    return response


def check_params(params):
    start_day = params.get(START_DAY)
    end_day = params.get(END_DAY)
    ou = params.get(LOCATION)
    page_index = params.get(INDEX_PAGE)

    if not (start_day and end_day and ou):
        raise IllegalArgumentException(message='%s, %s, %s are mandatory.' % (START_DAY, END_DAY, LOCATION))

    start = get_iso_calendar(start_day)
    end = get_iso_calendar(end_day)

    if start > end:
        raise IllegalArgumentException(message='%s must less than %s.' % (START_DAY, END_DAY))

    return start_day, end_day, ou, page_index


def get_iso_calendar(date):
    return datetime.fromtimestamp(float(date) / 1000).isocalendar()
