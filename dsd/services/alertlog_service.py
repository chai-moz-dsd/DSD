from django.db import connections

START_DAY = 'startDay'
END_DAY = 'endDay'
LOCATION = 'location'

PROVINCE = 'province'
DISTRICT = 'district'
FACILITY = 'facility'
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
    return 'SELECT "provinces"."province_name", "districts"."district_name","facilities"."facility_name",' \
           ' "alertLog"."BES_NUMBER","alertLog"."BES_YEAR", "alertLog"."alert_text", "alertLog"."dateSent"' \
           ' FROM "alertLog"' \
           ' LEFT JOIN "provinces" ON "alertLog"."provinceID" = "provinces"."id" ' \
           ' LEFT JOIN "districts" ON "alertLog"."districtID" = "districts"."id" ' \
           ' LEFT JOIN "facilities" ON "alertLog"."facilityID" = "facilities"."id" ' \
           ' WHERE "alertLog"."facilityID" <> \'0\' AND "alertLog"."districtID" <> \'0\' AND "alertLog"."provinceID" <> \'0\'' \
           ' AND "alertLog"."dateSent"' + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           get_location_clause(location_level, location_id) + ' ' + \
           ' ORDER BY ' + \
           get_order_clause()


def sql_get_moh_data(start_day, end_day):
    return 'SELECT "provinces"."province_name", "districts"."district_name","facilities"."facility_name",' \
           ' "alertLog"."BES_NUMBER","alertLog"."BES_YEAR", "alertLog"."alert_text", "alertLog"."dateSent"' \
           ' FROM "alertLog"' \
           ' LEFT JOIN "provinces" ON "alertLog"."provinceID" = "provinces"."id" ' \
           ' LEFT JOIN "districts" ON "alertLog"."districtID" = "districts"."id" ' \
           ' LEFT JOIN "facilities" ON "alertLog"."facilityID" = "facilities"."id" ' \
           ' WHERE "alertLog"."facilityID" <> \'0\' AND "alertLog"."districtID" <> \'0\' AND "alertLog"."provinceID" <> \'0\'' \
           ' AND "alertLog"."dateSent"' + ' ' + \
           get_where_clause(start_day, end_day) + ' ' + \
           ' ORDER BY ' + \
           get_order_clause()


def get_where_clause(start_day, end_day):
    return 'BETWEEN \'' + start_day + '\' AND \'' + end_day + '\''


def get_location_clause(location_level, location_id):
    return 'AND "alertLog"."' + location_level + 'ID" = \'' + str(location_id) + '\''


def get_order_clause():
    return '"dateSent" DESC'