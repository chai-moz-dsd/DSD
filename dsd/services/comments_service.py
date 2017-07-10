from django.db import connections

START = 'start'
END = 'end'
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


def default_sql():
    return 'SELECT "provinces"."province_name", "districts"."district_name",' \
           ' "facilities"."facility_name", "BES_MIDDLEWARE_CORE"."SKIPABLE_CAMPO_ABERTO",' \
           ' "BES_MIDDLEWARE_CORE"."BES_YEAR", "BES_MIDDLEWARE_CORE"."BES_NUMBER"' \
           ' FROM "BES_MIDDLEWARE_CORE"' \
           ' LEFT JOIN "provinces" ON "BES_MIDDLEWARE_CORE"."MIDDLEWARE_PROVINCE_ID" = "provinces"."id"' \
           ' LEFT JOIN "districts" ON "BES_MIDDLEWARE_CORE"."MIDDLEWARE_DISTRICT_ID" = "districts"."id"' \
           ' LEFT JOIN "facilities" ON "BES_MIDDLEWARE_CORE"."MIDDLEWARE_FACILITY_ID" = "facilities"."id"' \
           ' WHERE "BES_MIDDLEWARE_CORE"."SKIPABLE_CAMPO_ABERTO" IS NOT NULL' \
           ' AND "BES_MIDDLEWARE_CORE"."MIDDLEWARE_FACILITY_ID" <> \'0\' ' \
           ' AND "BES_MIDDLEWARE_CORE"."MIDDLEWARE_DISTRICT_ID" <> \'0\' ' \
           ' AND "BES_MIDDLEWARE_CORE"."MIDDLEWARE_PROVINCE_ID" <> \'0\' ' \
           ' AND "BES_MIDDLEWARE_CORE"."SKIPABLE_CAMPO_ABERTO" != \'\'' + ' '


def sql_get_data_by_filter(start_year, start_week, end_year, end_week, location_level, location_id):
    return default_sql() + ' ' + \
           get_where_clause(start_year, start_week, end_year, end_week) + ' ' + \
           get_location_clause(location_level, location_id) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def sql_get_data_by_filter_one_year(start_year, start_week, end_week, location_level, location_id):
    return default_sql() + ' ' + \
           get_where_one_year_clause(start_year, start_week, end_week) + ' ' + \
           get_location_clause(location_level, location_id) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def sql_get_moh_data(start_year, start_week, end_year, end_week):
    return default_sql() + ' ' + \
           get_where_clause(start_year, start_week, end_year, end_week) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def sql_get_moh_data_one_year(start_year, start_week, end_week):
    return default_sql() + ' ' + \
           get_where_one_year_clause(start_year, start_week, end_week) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def get_where_clause(start_year, start_week, end_year, end_week):
    return ' AND (' \
           ' ("BES_MIDDLEWARE_CORE"."BES_YEAR" > \'' + start_year + '-01-01\' ' \
              'AND "BES_MIDDLEWARE_CORE"."BES_YEAR" < \'' + end_year + '-01-01\' )' \
           ' OR' \
           ' ("BES_MIDDLEWARE_CORE"."BES_YEAR" = \'' + start_year + '-01-01\' ' \
              'AND "BES_MIDDLEWARE_CORE"."BES_NUMBER" >= \'' + start_week + '\' )' \
           ' OR' \
           ' ("BES_MIDDLEWARE_CORE"."BES_YEAR" = \'' + end_year + '-01-01\' ' \
              'AND "BES_MIDDLEWARE_CORE"."BES_NUMBER" <= \'' + end_week + '\' )' \
           ')'


def get_where_one_year_clause(start_year, start_week, end_week):
    return ' AND ' \
           ' ("BES_MIDDLEWARE_CORE"."BES_YEAR" = \'' + start_year + '-01-01\' ' \
              'AND "BES_MIDDLEWARE_CORE"."BES_NUMBER" >= \'' + start_week + '\' ' \
              'AND "BES_MIDDLEWARE_CORE"."BES_NUMBER" <= \'' + end_week + '\' ' \
           ')'


def get_location_clause(location_level, location_id):
    return 'AND "BES_MIDDLEWARE_CORE"."MIDDLEWARE_' + location_level + '_ID" = \'' + str(location_id) + '\''


def get_order_clause():
    return '"BES_MIDDLEWARE_CORE"."BES_YEAR" DESC, "BES_MIDDLEWARE_CORE"."BES_NUMBER" DESC'

