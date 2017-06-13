from django.db import connections

START_DAY = 'startDay'
END_DAY = 'endDay'
LOCATION = 'location'

PROVINCE = 'PROVINCE'
DISTRICT = 'DISTRICT'
FACILITY = 'FACILITY'
COUNTRY = 'COUNTRY'
PROVINCES = 'provinces'
DISTRICTS = 'districts'
FACILITIES = 'facilities'


def fetch_ou_id_by_ou_uid(uid):
    level = COUNTRY

    if uid == 'MOH12345678':
        return level, 'MOH'

    with connections['default'].cursor() as cursor:
        cursor.execute(sql_find_location(uid, PROVINCE))
        rows = cursor.fetchall()
        level = PROVINCE

        if not rows:
            cursor.execute(sql_find_location(uid, DISTRICT))
            rows = cursor.fetchall()
            level = DISTRICT

        if not rows:
            cursor.execute(sql_find_location(uid, FACILITY))
            rows = cursor.fetchall()
            level = FACILITY

    return level, rows[0][0]


def sql_find_location_name(id, column, table):
    return 'SELECT %s_name FROM %s WHERE id = \'%s\';' % (column, table, id)


def sql_find_location(ou_id, area):
    return 'SELECT id FROM dsd_%s WHERE uid = \'%s\';' % (area, ou_id)


def sql_get_data_by_filter(location_level, location_id, start_day, end_day):
    return 'SELECT ' + \
           get_province_name_selection() + ',' + \
           get_district_name_selection() + ',' + \
           get_facility_name_selection() + ',' + \
           get_message_selection() + ',' + \
           get_create_selection() + ',' + \
           get_submitted_selection() + ' ' + \
           'FROM ' + \
           get_from_clause() + ' ' + \
           'WHERE ' + \
           get_submitted_selection() + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           get_location_clause(location_level, location_id) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def sql_get_moh_data(start_day, end_day):
    return 'SELECT ' + \
           get_province_name_selection() + ',' + \
           get_district_name_selection() + ',' + \
           get_facility_name_selection() + ',' + \
           get_message_selection() + ',' + \
           get_create_selection() + ',' + \
           get_submitted_selection() + ' ' + \
           'FROM ' + \
           get_from_clause() + ' ' + \
           'WHERE ' + \
           get_submitted_selection() + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def get_province_name_selection():
    return '"MIDDLEWARE_PROVINCE_ID"'


def get_district_name_selection():
    return '"MIDDLEWARE_DISTRICT_ID"'


def get_facility_name_selection():
    return '"MIDDLEWARE_FACILITY_ID"'


def get_message_selection():
    return '"CAMPO_ABERTO"'


def get_create_selection():
    return '"_CREATION_DATE"'


def get_submitted_selection():
    return '"_SUBMISSION_DATE"'


def get_from_clause():
    return '"REMETENTE_MIDDLEWARE_CORE"'


def get_where_clause(start_day, end_day):
    return 'BETWEEN \'' + start_day + '\' AND \'' + end_day + '\''


def get_location_clause(location_level, location_id):
    return 'AND "MIDDLEWARE_' + location_level + '_ID" = \'' + str(location_id) + '\''


def get_order_clause():
    return '"_SUBMISSION_DATE" DESC'

