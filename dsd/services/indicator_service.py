START_DATE = 'startDate'
END_DATE = 'endDate'
OUS = 'organisationUnits'

MIN_WEEK = 1
MAX_WEEK = 53


def get_sql_command(facilities, start, end):
    return 'SELECT ' + \
           get_facility_name_selection() + ',' + \
           get_completeness_selection() + ',' + \
           get_freshness_selection() + ',' + \
           get_submission_date_selection() + ',' + \
           get_bes_number_selection() + ',' + \
           get_week_of_year_selection() + ',' + \
           get_week_of_year_selection() + ' ' + \
           'FROM ' + \
           get_from_clause() + ' ' + \
           'WHERE ' + \
           get_where_clause(facilities, start, end) + ' ' + \
           'ORDER BY ' + \
           get_order_clause()


def get_facility_name_selection():
    return 'facility_name'


def get_submission_date_selection():
    return '"_SUBMISSION_DATE"'


def get_bes_number_selection():
    return '"BES_NUMBER"'


def get_week_of_year_selection():
    return 'date_part(\'week\', "_SUBMISSION_DATE") as weekOfYear'


def get_day_of_week():
    return 'date_part(\'isodow\', "_SUBMISSION_DATE") AS dayOfWeek'


def get_completeness_selection():
    def get_selection(name):
        return '"%s" = -1 OR "%s" IS NULL ' % (name, name)

    return '(CASE WHEN "CASOS_COLERA" = -1 OR "CASOS_COLERA" IS NULL ' + \
           'OR ' + get_selection('CASOS_DIARREIA_0_4') + \
           'OR ' + get_selection('CASOS_DIARREIA_15') + \
           'OR ' + get_selection('CASOS_DIARREIA_5_14') + \
           'OR ' + get_selection('CASOS_DISENTERIA') + \
           'OR ' + get_selection('CASOS_MALARIA_CLINICA_0_4') + \
           'OR ' + get_selection('CASOS_MALARIA_CLINICA_5') + \
           'OR ' + get_selection('CASOS_MALARIA_CONFIRMADA_0_4') + \
           'OR ' + get_selection('CASOS_MALARIA_CONFIRMADA_5') + \
           'OR ' + get_selection('CASOS_MENINGITE_0_4') + \
           'OR ' + get_selection('CASOS_MENINGITE_5') + \
           'OR ' + get_selection('CASOS_PESTE') + \
           'OR ' + get_selection('CASOS_PFA') + \
           'OR ' + get_selection('CASOS_RAIVA') + \
           'OR ' + get_selection('CASOS_SARAMPO_24') + \
           'OR ' + get_selection('CASOS_SARAMPO_9') + \
           'OR ' + get_selection('CASOS_SARAMPO_NV_9_23') + \
           'OR ' + get_selection('CASOS_SARAMPO_V_9_23') + \
           'OR ' + get_selection('CASOS_TETANO') + \
           'OR ' + get_selection('OBITOS_COLERA') + \
           'OR ' + get_selection('OBITOS_DIARREIA_0_4') + \
           'OR ' + get_selection('OBITOS_DIARREIA_15') + \
           'OR ' + get_selection('OBITOS_DIARREIA_5_14') + \
           'OR ' + get_selection('OBITOS_DISENTERIA') + \
           'OR ' + get_selection('OBITOS_MALARIA_CLINICA_0_4') + \
           'OR ' + get_selection('OBITOS_MALARIA_CLINICA_5') + \
           'OR ' + get_selection('OBITOS_MALARIA_CONFIRMADA_0_4') + \
           'OR ' + get_selection('OBITOS_MALARIA_CONFIRMADA_5') + \
           'OR ' + get_selection('OBITOS_MENINGITE_0_4') + \
           'OR ' + get_selection('OBITOS_MENINGITE_5') + \
           'OR ' + get_selection('OBITOS_PESTE') + \
           'OR ' + get_selection('OBITOS_PFA') + \
           'OR ' + get_selection('OBITOS_RAIVA') + \
           'OR ' + get_selection('OBITOS_SARAMPO_24') + \
           'OR ' + get_selection('OBITOS_SARAMPO_9') + \
           'OR ' + get_selection('OBITOS_SARAMPO_NV_9_23') + \
           'OR ' + get_selection('OBITOS_SARAMPO_V_9_23') + \
           'OR ' + get_selection('OBITOS_TETANO') + \
           'THEN \'Incompleted\' ' \
           'ELSE \'Completed\' END) AS syncStatus'


def get_freshness_selection():
    return '(CASE ' \
           'WHEN date_part(\'week\', "_SUBMISSION_DATE") < "BES_NUMBER" ' \
           'OR (date_part(\'week\', "_SUBMISSION_DATE") = "BES_NUMBER" ' \
           'AND date_part(\'isodow\', "_SUBMISSION_DATE") < 7) THEN \'Early\' ' \
           'WHEN date_part(\'week\', "_SUBMISSION_DATE") > "BES_NUMBER" + 1 ' \
           'OR (date_part(\'week\', "_SUBMISSION_DATE") = "BES_NUMBER" + 1 ' \
           'AND date_part(\'isodow\', "_SUBMISSION_DATE") > 2) THEN \'Later\' ' \
           'ELSE \'Normal\' ' \
           'END) ' \
           'AS freshness'


def get_from_clause():
    return 'facilities INNER JOIN "BES_MIDDLEWARE_CORE" ON device_serial = "DEVICEID"'


def get_where_clause(facilities, start, end):
    return '%s AND %s' % (get_facility_where_clause(facilities), get_week_where_clause(start, end))


def get_facility_where_clause(facilities):
    if not len(facilities):
        return ''

    return '(%s)' % ' OR '.join(['facility_name = \'%s\'' % facility for facility in facilities])


def get_week_where_clause(start, end):
    start_year = start[0]
    start_week = start[1]
    end_year = end[0]
    end_week = end[1]

    template = '"BES_YEAR" = \'%s-01-01\' AND "BES_NUMBER" BETWEEN %s AND %s'

    if start_year == end_year:
        return '(%s)' % template % (start_year, start_week, end_week)
    else:
        return '((%s) OR (%s))' % (template % (start_year, start_week, MAX_WEEK),
                                   template % (end_year, MIN_WEEK, end_week))


def get_order_clause():
    return '"BES_NUMBER" ASC, "_SUBMISSION_DATE" DESC'
