# encoding: utf-8
import xlsxwriter
from django.db import connections
from dsd.services.submission_service import sql_excel_data, sql_excel_data_no_location

PATH = '/tmp/'


def create_excel(workbook, worksheet, location_level, location_id, start_day, end_day):

    create_excel_header(workbook, worksheet)

    with connections['default'].cursor() as cursor:
        if location_level == 'COUNTRY':
            cursor.execute(sql_excel_data_no_location(start_day, end_day))
            data = cursor.fetchall()
        else:
            cursor.execute(sql_excel_data(location_level, location_id, start_day, end_day))
            data = cursor.fetchall()

    create_excel_data(worksheet, data)


def create_excel_header(workbook, worksheet):
    header_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': '#4785BE',
        'fg_color': '#EBEBEB',
        'font_size': 10})

    worksheet.set_column('A:E', 15)
    worksheet.set_column('F:AQ', 10)
    worksheet.set_column('AR:AT', 20)
    worksheet.set_row(0, 25)
    worksheet.set_row(1, 25)
    worksheet.set_row(2, 25)

    worksheet.merge_range('A1:A3', 'Facility', header_format)
    worksheet.merge_range('B1:B3', 'District', header_format)
    worksheet.merge_range('C1:C3', 'Province', header_format)
    worksheet.merge_range('D1:D3', 'Week End Date', header_format)
    worksheet.merge_range('E1:E3', 'Week', header_format)

    worksheet.merge_range('F1:G2', '001 CÓLERA', header_format)
    worksheet.merge_range('H1:I2', '009.2 DISENTERIA', header_format)
    worksheet.merge_range('J1:K2', '020 PESTE', header_format)
    worksheet.merge_range('L1:M2', '037 TÉTANO RECÉM NASCIDOS', header_format)
    worksheet.merge_range('N1:O2', '045 PARALISIA FLÁCIDA AGUDA', header_format)
    worksheet.merge_range('P1:Q2', '071 RAIVA', header_format)

    worksheet.merge_range('R1:W1', 'DIARREIA 009', header_format)
    worksheet.merge_range('R2:S2', '0-4 anos', header_format)
    worksheet.merge_range('T2:U2', '5-14 anos', header_format)
    worksheet.merge_range('V2:W2', '15 anos+', header_format)

    worksheet.merge_range('X1:AA1', 'MALARIA CLINICA', header_format)
    worksheet.merge_range('X2:Y2', '0-4 anos', header_format)
    worksheet.merge_range('Z2:AA2', '5 anos+', header_format)

    worksheet.merge_range('AB1:AE1', 'MALARIA CONFIRMADA', header_format)
    worksheet.merge_range('AB2:AC2', '0-4 anos', header_format)
    worksheet.merge_range('AD2:AE2', '5 anos+', header_format)

    worksheet.merge_range('AF1:AI1', 'MENINGITE 036', header_format)
    worksheet.merge_range('AF2:AG2', '0-4 anos', header_format)
    worksheet.merge_range('AH2:AI2', '5 anos+', header_format)

    worksheet.merge_range('AJ1:AQ1', 'SARAMPO 055', header_format)
    worksheet.merge_range('AJ2:AK2', 'Menos de 9 meses', header_format)
    worksheet.merge_range('AL2:AM2', '9-23 meses(Não Vacinados)', header_format)
    worksheet.merge_range('AN2:AO2', '9-23 meses(Vacinados)', header_format)
    worksheet.merge_range('AP2:AQ2', '24 meses e mais', header_format)

    worksheet.merge_range('AR1:AT3', 'Observacoes', header_format)

    # loop from F to AQ
    for index in range(5, 43):
        if (index % 2) == 0:
            worksheet.write(2, index, 'O', header_format)
        else:
            worksheet.write(2, index, 'C', header_format)


def create_excel_data(worksheet, data):
    for row in range(len(data)):
        for index in range(len(data[row])):
            if index == 3:
                worksheet.write(row + 3, index, data[row][index].strftime('%Y-%m-%d'))
            else:
                worksheet.write(row + 3, index, data[row][index])