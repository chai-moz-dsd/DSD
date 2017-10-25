from django.db import connections

START_DAY = 'startDay'
END_DAY = 'endDay'
LOCATION = 'location'
INDEX_PAGE = 'page_index'
PAGE_SIZE = '20'

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


def default_sql():
    return 'SELECT "dsd_facility"."facility_name", "dsd_district"."district_name", "dsd_province"."province_name",' \
           ' "dsd_besmiddlewarecore"."date_week_end", "dsd_besmiddlewarecore"."bes_number",' \
           ' "dsd_besmiddlewarecore"."cases_cholera", "dsd_besmiddlewarecore"."deaths_cholera",' \
           ' "dsd_besmiddlewarecore"."cases_dysentery", "dsd_besmiddlewarecore"."deaths_dysentery",' \
           ' "dsd_besmiddlewarecore"."cases_plague", "dsd_besmiddlewarecore"."deaths_plague",' \
           ' "dsd_besmiddlewarecore"."cases_tetanus", "dsd_besmiddlewarecore"."deaths_tetanus",' \
           ' "dsd_besmiddlewarecore"."cases_pfa", "dsd_besmiddlewarecore"."deaths_pfa",' \
           ' "dsd_besmiddlewarecore"."cases_rabies", "dsd_besmiddlewarecore"."deaths_rabies",' \
           ' "dsd_besmiddlewarecore"."cases_diarrhea_04", "dsd_besmiddlewarecore"."deaths_diarrhea_04", "dsd_besmiddlewarecore"."cases_diarrhea_5_14", "dsd_besmiddlewarecore"."deaths_diarrhea_5_14", "dsd_besmiddlewarecore"."cases_diarrhea_15", "dsd_besmiddlewarecore"."deaths_diarrhea_15",' \
           ' "dsd_besmiddlewarecore"."cases_malaria_clinic_0_4", "dsd_besmiddlewarecore"."deaths_malaria_clinic_0_4", "dsd_besmiddlewarecore"."cases_malaria_clinic_5", "dsd_besmiddlewarecore"."deaths_malaria_clinic_5",' \
           ' "dsd_besmiddlewarecore"."cases_malaria_confirmed_0_4", "dsd_besmiddlewarecore"."deaths_malaria_confirmed_0_4", "dsd_besmiddlewarecore"."cases_malaria_confirmed_5", "dsd_besmiddlewarecore"."deaths_malaria_confirmed_5",' \
           ' "dsd_besmiddlewarecore"."cases_meningitis_0_4", "dsd_besmiddlewarecore"."deaths_meningitis_04", "dsd_besmiddlewarecore"."cases_meningitis_5", "dsd_besmiddlewarecore"."deaths_meningitis_5",' \
           ' "dsd_besmiddlewarecore"."cases_measles_9", "dsd_besmiddlewarecore"."deaths_measles_9", "dsd_besmiddlewarecore"."cases_nv_measles", "dsd_besmiddlewarecore"."deaths_measles_nv",' \
           ' "dsd_besmiddlewarecore"."cases_measles_v9_23", "dsd_besmiddlewarecore"."deaths_measles_v_9_23", "dsd_besmiddlewarecore"."cases_measles_24", "dsd_besmiddlewarecore"."deaths_measles_24",' \
           ' "dsd_besmiddlewarecore"."skippable_open_field"' \
           ' FROM "dsd_besmiddlewarecore"' \
           ' LEFT JOIN "dsd_facility" ON "dsd_besmiddlewarecore"."middleware_facility_id" = "dsd_facility"."id"' \
           ' LEFT JOIN "dsd_district" ON "dsd_besmiddlewarecore"."middleware_district_id" = "dsd_district"."id"' \
           ' LEFT JOIN "dsd_province" ON "dsd_besmiddlewarecore"."middleware_province_id" = "dsd_province"."id"'


def default_sql_for_select_count():
    return ' SELECT COUNT(*) FROM "dsd_besmiddlewarecore"'


def sql_get_total_number_no_location(start_day, end_day):
    return default_sql_for_select_count() + ' ' + \
           get_where_clause(start_day, end_day)


def sql_get_total_number(location_level, location_id, start_day, end_day):
    return default_sql_for_select_count() + ' ' + \
           get_where_clause(start_day, end_day) + \
           get_location_clause(location_level, location_id)


def sql_get_details_no_location(start_day, end_day, page_index):
    return default_sql() + ' ' + \
           get_where_clause(start_day, end_day) + \
           get_order_clause() + \
           get_limit_clause(page_index)


def sql_get_details(location_level, location_id, start_day, end_day, page_index):
    return default_sql() + ' ' + \
           get_where_clause(start_day, end_day) + \
           get_location_clause(location_level, location_id) + \
           get_order_clause() + \
           get_limit_clause(page_index)


def sql_excel_data_no_location(start_day, end_day):
    return default_sql() + ' ' + \
           get_where_clause(start_day, end_day) + \
           get_order_clause()


def sql_excel_data(location_level, location_id, start_day, end_day):
    return default_sql() + ' ' + \
           get_where_clause(start_day, end_day) + \
           get_location_clause(location_level, location_id) + \
           get_order_clause()


def get_limit_clause(page_index):
    return ' LIMIT ' + PAGE_SIZE + ' OFFSET ( ' + page_index + ' - 1 ) * ' + PAGE_SIZE


def get_where_clause(start_day, end_day):
    return ' WHERE "submission_date" BETWEEN \'' + start_day + '\' AND \'' + end_day + '\''


def get_location_clause(location_level, location_id):
    return ' AND "dsd_besmiddlewarecore"."middleware_' + location_level + '_id" = \'' + str(location_id) + '\''


def get_order_clause():
    return ' ORDER BY "dsd_province"."province_name" ASC, "dsd_district"."district_name" ASC, "dsd_facility"."facility_name" ASC'
