from django.db import connections

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException

WEEK = 'week'
ORGANIZATION_UNITS = 'ou'
MOH = None
PROVINCE = 'province'
DISTRICT = 'district'
FACILITY = 'facility'
USED_FACILITY_CONDITION = ' AND device_serial IS NOT NULL'

MAX_RECORDS = 1000
COMPLETED = 0
MISSING = 1
INCOMPLETE = 2

DATA_ELEMENTS = ["CASOS_COLERA", "CASOS_DIARREIA_0_4", "CASOS_DIARREIA_15", "CASOS_DIARREIA_5_14", "CASOS_DISENTERIA",
                 "CASOS_MALARIA_CLINICA_0_4", "CASOS_MALARIA_CLINICA_5", "CASOS_MALARIA_CONFIRMADA_0_4",
                 "CASOS_MALARIA_CONFIRMADA_5", "CASOS_MENINGITE_0_4", "CASOS_MENINGITE_5", "CASOS_PESTE", "CASOS_PFA",
                 "CASOS_RAIVA", "CASOS_SARAMPO_24", "CASOS_SARAMPO_9", "CASOS_SARAMPO_NV_9_23", "CASOS_SARAMPO_V_9_23",
                 "CASOS_TETANO", "OBITOS_COLERA", "OBITOS_DIARREIA_0_4", "OBITOS_DIARREIA_15", "OBITOS_DIARREIA_5_14",
                 "OBITOS_DISENTERIA", "OBITOS_MALARIA_CLINICA_0_4", "OBITOS_MALARIA_CLINICA_5",
                 "OBITOS_MALARIA_CONFIRMADA_0_4", "OBITOS_MALARIA_CONFIRMADA_5", "OBITOS_MENINGITE_0_4",
                 "OBITOS_MENINGITE_5", "OBITOS_PESTE", "OBITOS_PFA", "OBITOS_RAIVA", "OBITOS_SARAMPO_24",
                 "OBITOS_SARAMPO_9", "OBITOS_SARAMPO_NV_9_23", "OBITOS_SARAMPO_V_9_23", "OBITOS_TETANO"]


def get_completed_condition(element):
    return '"%s" != -1 AND "%s" IS NOT NULL' % (element, element)


def get_missing_condition(element):
    return '"%s" = -1 OR "%s" IS NULL' % (element, element)


def sql_completeness_case(data_elements):
    completed_conditions = [get_completed_condition(ele) for ele in data_elements]
    missing_conditions = [get_missing_condition(ele) for ele in data_elements]
    return 'CASE WHEN %s THEN \'Completed\' WHEN ( %s ) THEN \'Missing\' ELSE \'Incompleted\' END' % \
           (' AND '.join(completed_conditions),
            ' ) AND ( '.join(missing_conditions))


def get_sum_condition(column_name, match_condition, new_column_name):
    return 'SUM(CASE WHEN %s = \'%s\' THEN 1 ELSE 0 END) AS %s' % \
           (column_name, match_condition, new_column_name)


def sql_completeness_sum(column_name):
    return '%s, %s, %s' % (get_sum_condition(column_name, 'Completed', 'completed'),
                           get_sum_condition(column_name, 'Missing', 'missing'),
                           get_sum_condition(column_name, 'Incompleted', 'incomplete'))


def check_parameter(parameters):
    week_num = parameters.get(WEEK).split('W')[1]
    year_num = parameters.get(WEEK).split('W')[0]
    ous = parameters.get(ORGANIZATION_UNITS)

    if not (week_num and ous):
        raise IllegalArgumentException(message='%s, %s are mandatory.' % (week_num, ous))

    return year_num, week_num, ous


def sql_completeness_where(ous, year_num, week_num, area):
    if not area:
        area_condition = ''
    elif area == 'facility':
        area_condition = 'f.facility_name = \'%s\' AND' % (ous)
    else:
        area_condition = 'p.%s_name = \'%s\' AND' % (area, ous)
    return 'WHERE %s "BES_YEAR" = \'%s-01-01\' AND "BES_NUMBER" = %s ' % (area_condition, year_num, week_num)


def get_sql_subtable_command(ous, year_num, week_num, area):
    if not area or area == 'facility':
        inner_join_table = ''
    else:
        inner_join_table = 'INNER JOIN "%ss" as p ON f.%s_id = p.id ' % \
                           (area, area)

    return 'SELECT distinct on (facility_name) facility_name, "_SUBMISSION_DATE", (' \
           '%s ) AS syncStatus ' \
           'FROM facilities as f ' \
           'INNER JOIN "BES_MIDDLEWARE_CORE" ON device_serial = "DEVICEID" ' \
           '%s' \
           '%s' \
           'order by facility_name, "_SUBMISSION_DATE" desc' % \
           (sql_completeness_case(DATA_ELEMENTS),
            inner_join_table,
            sql_completeness_where(ous, year_num, week_num, area))


def get_sql_command(ous, year_num, week_num, area):
    result = 'SELECT %s ' \
             'FROM (%s) as STATUS_TABLE;' % \
             (sql_completeness_sum('STATUS_TABLE.syncStatus'),
              get_sql_subtable_command(ous, year_num, week_num, area))

    # print(result)

    return result


def get_completeness_data(rows, status):
    if not rows[0][status]:
        return 0
    return rows[0][status]


def ous_is_moh(ous):
    return ous == 'MOH'


def ous_is_valid(rows):
    return not any(rows[0])


def fetch_completeness_from_remote_database(year_num, week_num, ous):
    rows = [(None, None, None)]
    with connections['chai'].cursor() as cursor:
        if ous_is_moh(ous):
            cursor.execute(get_sql_command(ous, year_num, week_num, MOH))
            rows = cursor.fetchall()

        for area in (PROVINCE, DISTRICT, FACILITY):
            if ous_is_valid(rows):
                cursor.execute(get_sql_command(ous, year_num, week_num, area))
                rows = cursor.fetchall()

        completed = get_completeness_data(rows, COMPLETED)
        missing = get_completeness_data(rows, MISSING)
        incomplete = get_completeness_data(rows, INCOMPLETE)

    return completed, incomplete, missing


def fetch_facility_num_from_remote_database(ous, used_facility_condition):
    rows = [(None, None, None)]
    with connections['chai'].cursor() as cursor:
        if ous_is_moh(ous):
            cursor.execute(sql_facilities_in_area(ous, MOH, used_facility_condition))
            rows = cursor.fetchall()
            return get_count_from_database(rows)

        for area in (PROVINCE, DISTRICT):
            if not get_count_from_database(rows):
                cursor.execute(sql_facilities_in_area(ous, area, used_facility_condition))
                rows = cursor.fetchall()

        if not get_count_from_database(rows):
            return 1

    return get_count_from_database(rows)


def fetch_total_facility_from_remote_database(ous):
    return fetch_facility_num_from_remote_database(ous, '')


def fetch_used_facility_from_remote_database(ous):
    return fetch_facility_num_from_remote_database(ous, USED_FACILITY_CONDITION)


def fetch_ou_name_by_ou_id(ou_id):
    if ou_id == 'MOH12345678':
        return 'MOH'

    with connections['default'].cursor() as cursor:
        cursor.execute(sql_ou_province(ou_id, PROVINCE))
        rows = cursor.fetchall()

        if not rows:
            cursor.execute(sql_ou_province(ou_id, DISTRICT))
            rows = cursor.fetchall()

        if not rows:
            cursor.execute(sql_ou_province(ou_id, FACILITY))
            rows = cursor.fetchall()

    return rows[0][0]


def get_count_from_database(rows):
    return rows[0][0]


def sql_ou_province(ou_id, area):
    return 'SELECT %s_name FROM dsd_%s WHERE uid = \'%s\';' % (area, area, ou_id)


def sql_facilities_in_area(ous, area, used_facility_condition):
    if area is None and used_facility_condition == '':
        return 'SELECT COUNT(*) FROM facilities;'
    elif area is None:
        return 'SELECT COUNT(*) FROM facilities WHERE %s;' % used_facility_condition.replace('AND', '')

    return 'SELECT COUNT(*) FROM facilities AS f INNER JOIN %ss AS p ON f.%s_id = p.id ' \
           'WHERE p.%s_name = \'%s\'%s;' % (area, area, area, ous, used_facility_condition)
