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


def sql_find_location(ou_id, area):
    return 'SELECT id FROM dsd_%s WHERE uid = \'%s\';' % (area, ou_id)


def sql_get_data_by_filter(location_level, location_id, start_day, end_day):
    return 'SELECT "provinces"."province_name", "districts"."district_name",' \
           '"facilities"."facility_name", "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO",' \
           '"REMETENTE_MIDDLEWARE_CORE"."_CREATION_DATE", "REMETENTE_MIDDLEWARE_CORE"."_SUBMISSION_DATE"' \
           ' FROM "REMETENTE_MIDDLEWARE_CORE"' \
           ' LEFT JOIN "provinces" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_PROVINCE_ID" = "provinces"."id"' \
           ' LEFT JOIN "districts" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_DISTRICT_ID" = "districts"."id"' \
           ' LEFT JOIN "facilities" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_FACILITY_ID" = "facilities"."id"' \
           ' WHERE "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO" IS NOT NULL' \
           ' AND "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO" != \'\' ' \
           ' AND "REMETENTE_MIDDLEWARE_CORE"."_SUBMISSION_DATE"' + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           get_location_clause(location_level, location_id) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def sql_get_moh_data(start_day, end_day):
    return 'SELECT "provinces"."province_name", "districts"."district_name",' \
           '"facilities"."facility_name", "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO",' \
           '"REMETENTE_MIDDLEWARE_CORE"."_CREATION_DATE", "REMETENTE_MIDDLEWARE_CORE"."_SUBMISSION_DATE"' \
           ' FROM "REMETENTE_MIDDLEWARE_CORE"' \
           ' LEFT JOIN "provinces" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_PROVINCE_ID" = "provinces"."id"' \
           ' LEFT JOIN "districts" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_DISTRICT_ID" = "districts"."id"' \
           ' LEFT JOIN "facilities" ON "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_FACILITY_ID" = "facilities"."id"' \
           ' WHERE "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO" IS NOT NULL' \
           ' AND "REMETENTE_MIDDLEWARE_CORE"."CAMPO_ABERTO" != \'\' ' \
           ' AND "REMETENTE_MIDDLEWARE_CORE"."_SUBMISSION_DATE"' + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def get_where_clause(start_day, end_day):
    return 'BETWEEN \'' + start_day + '\' AND \'' + end_day + '\''


def get_location_clause(location_level, location_id):
    return 'AND "REMETENTE_MIDDLEWARE_CORE"."MIDDLEWARE_' + location_level + '_ID" = \'' + str(location_id) + '\''


def get_order_clause():
    return '"_SUBMISSION_DATE" DESC'

