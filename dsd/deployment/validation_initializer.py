import logging

from dsd.config.dhis2_config import VALIDATION_RULE_GROUP
from dsd.models import Element
from dsd.repositories.dhis2_remote_repository import get_user_groups
from dsd.services.data_value_validation_service import DataElementValuesValidationService
from dsd.services.validation_rule_service import ORGANISATION_UNIT_LEVEL, post_validation_rule, \
    post_validation_rule_group, OPERATOR, ADDITIONAL_RULE_TYPE

logger = logging.getLogger(__name__)


def add_colera_case():
    rule_id = 'tOCXddkXkw0'
    disease_code = '001_CÓLERA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_cholera')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Cólera Casos > 0',
                         rule_description='Threshold around Colera casos',
                         rule_instruction='Follow instructions around Colera outbreak',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Cólera caso',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')



def add_colera_deth():
    rule_id = 'iz4ccOJSd4l'
    disease_code = '001_CÓLERA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'deaths_cholera')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Cólera morte > 2',
                         rule_description='More than 2 adult deaths in a EPI week in a district',
                         rule_instruction='More than 2 adult deaths in a EPI week in a district',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Cólera morte',
                         date_element_ids=date_element_ids,
                         right_side_expression='2')



def add_diarreia_death():
    rule_id = 'NGNXRZoeBgj'
    disease_code = 'DIARREIA_009'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'deaths_diarrhea_15')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Diarreia adulto death Case',
                         rule_description='2 adult deaths in a district.\r\n“Adult” here refers to cases with age greater than 15 years old.',
                         rule_instruction='2 adult deaths in a district.\r\n“Adult” here refers to cases with age greater than 15 years old.',
                         operator=OPERATOR.less_than,
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Diarreia',
                         date_element_ids=date_element_ids,
                         right_side_expression='2')


def add_disenteria_case():
    rule_id = 'QhVKtePYsLu'
    disease_code = '009.2_DISENTERIA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_dysentery')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Disenteria (Shigella): Caso > 0',
                         rule_description='Disenteria (Shigella): Caso > 0',
                         rule_instruction='Disenteria (Shigella): Caso > 0',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Disenteria saso',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')

def add_pfa_case():
    rule_id = 'GzblVtRJAQD'
    disease_code = '045_PARALISIA_FLÁCIDA_AGUDA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code, 'cases_pfa')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Paralesia flacida aguda (PFA) > 0',
                         rule_description='Any Paralesia flacida aguda (PFA) in a district.',
                         rule_instruction='Any Paralesia flacida aguda (PFA) in a district.',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Paralesia flacida aguda (PFA) caso',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')


def add_peste_case():
    rule_id = 'MlHtb3yxsJn'
    disease_code = '020_PESTE'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_plague')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Peste caso > 0',
                         rule_description='Any case of Peste',
                         rule_instruction='Any case of Peste',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Peste caso',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')


def add_raiva_case():
    rule_id = 'SBm9jfYqwFc'
    disease_code = '071_RAIVA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_rabies')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Raiva caso > 0',
                         rule_description='Any case in a district.',
                         rule_instruction='Any case in a district.',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Raiva caso',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')


def add_raiva_death():
    rule_id = 'AhTAFtw7sM4'
    disease_code = '071_RAIVA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'deaths_rabies')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Raiva  morte > 0',
                         rule_description='Any death in a district.',
                         rule_instruction='Any death in a district.',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Raiva morte',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')


def add_sarampo_case():
    rule_id = 'C0U9HaMlefd'
    disease_code = 'SARAMPO_055'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = '%s+%s' % (
        DataElementValuesValidationService.assemble_left_side_expression(disease_code, 'cases_measles'),
        DataElementValuesValidationService.assemble_left_side_expression(disease_code, 'cases_nv_measles'))

    post_validation_rule(rule_id=rule_id,
                         rule_name='Sarampo case in a HF in a week',
                         rule_description='3 cases in a HF in a week',
                         rule_instruction='3 cases in a HF in a week',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Sarampo caso',
                         date_element_ids=date_element_ids,
                         right_side_expression='3',
                         operator=OPERATOR.less_than)


def add_tetanus_case():
    rule_id = 'Q9Ko2HFaPJm'
    disease_code = '037_TÉTANO_RECÉM_NASCIDOS'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_tetanus')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Tétano no recém nascido caso > 0',
                         rule_description='Any case in a district',
                         rule_instruction='Any case in a district',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Tétano no recém nascido caseo',
                         date_element_ids=date_element_ids,
                         right_side_expression='0')


def add_malaria_case():
    rule_id = 'm9vqJzIXCcr'
    disease_code1 = 'MALARIA_CLINICA'
    date_element_id1 = Element.objects.get(code=disease_code1).id
    disease_code2 = 'MALARIA_CONFIRMADA'
    date_element_id2 = Element.objects.get(code=disease_code2).id

    left_side_expression = '%s+%s' % (
        DataElementValuesValidationService.assemble_left_side_expression(disease_code1, 'cases_malaria_clinic')
        , DataElementValuesValidationService.assemble_left_side_expression(disease_code2, 'cases_malaria_confirmed'))

    post_validation_rule(rule_id=rule_id,
                         rule_name='Malária: Casos > average from current week + (A) ealiar weeks to current week - (B) weeks later weeks in past (C) years + (D) * std dev',
                         rule_description='Cases reported within the reporting period > the mean of the same epidemilogical period for the previous 5 years + 2 std dev. NB: monthly, not weekly\r\nThe logic can be described as:\r\nCase reported in this calendar month (current EPI week and 2 weeks before and after) > the average of cases in same calendar month period for past 5 years + 2 std dev',
                         rule_instruction='Cases reported within the reporting period > the mean of the same epidemilogical period for the previous 5 years + 2 std dev. NB: monthly, not weekly\r\nThe logic can be described as:\r\nCase reported in this calendar month (current EPI week and 2 weeks before and after) > the average of cases in same calendar month period for past 5 years + 2 std dev',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Malária cases greater than average in past years',
                         date_element_ids=[date_element_id1, date_element_id2],
                         right_side_expression='0',
                         additional_rule_type=ADDITIONAL_RULE_TYPE.MalariaCaseInYears,
                         additional_rule='A:2\r\nB:2\r\nC:5\r\nD:2'
                         )


def add_complex_disenteria_case():
    rule_id = 'vKERgxn2ycf'
    disease_code = '009.2_DISENTERIA'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_dysentery')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Disenteria: Cases > average for same week in last ( A ) years + ( B ) * std dev',
                         rule_description='Cases reported within the epidemiological week > the mean of the same epidemilogical week for the previous 5 years + 2 std dev.',
                         rule_instruction='Cases reported within the epidemiological week > the mean of the same epidemilogical week for the previous 5 years + 2 std dev.',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Disenteria cases greater than average for same week in last years',
                         date_element_ids=date_element_ids,
                         right_side_expression='0',
                         additional_rule_type=ADDITIONAL_RULE_TYPE.DisenteriaCaseInYears,
                         additional_rule='A: 5\r\nB: 2'
                         )


def add_meningite_case():
    rule_id = 'JTiPI2lUKp0'
    disease_code = 'MENINGITE_036'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = DataElementValuesValidationService.assemble_left_side_expression(disease_code,
                                                                                            'cases_meningitis')

    post_validation_rule(rule_id=rule_id,
                         rule_name='Meningite (inclui suspeitas) week1 * 2 < week2; week2 * 2 < week3',
                         rule_description='Case duplication in last 3 consectuve epidemiological weeks\r\nThe logic can be described as:\r\nCase for week 1 * 2 <= Case for week 2 && Case for week 2 * 2 <= Case for week 3\r\nFor example, week 1 we have 2 cases, week 2 we have 4 or more cases, and for week 3 we have 8 or more cases, then this would trigger the alert.',
                         rule_instruction='Case duplication in last 3 consectuve epidemiological weeks\r\nThe logic can be described as:\r\nCase for week 1 * 2 <= Case for week 2 && Case for week 2 * 2 <= Case for week 3\r\nFor example, week 1 we have 2 cases, week 2 we have 4 or more cases, and for week 3 we have 8 or more cases, then this would trigger the alert.',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         left_side_expression=left_side_expression,
                         left_side_description='Meningite cases duplication in recent consecutive weeks',
                         date_element_ids=date_element_ids,
                         right_side_expression='0',
                         additional_rule_type=ADDITIONAL_RULE_TYPE.MeningiteIncreasedInWeeks,
                         additional_rule='A:2\r\nB:3'
                         )


def add_complex_sarampo_case():
    rule_id = 'FU31nh8lfLn'
    disease_code = 'SARAMPO_055'
    date_element_ids = [Element.objects.get(code=disease_code).id]
    left_side_expression = '%s+%s' % (
        DataElementValuesValidationService.assemble_left_side_expression(disease_code, 'cases_measles'),
        DataElementValuesValidationService.assemble_left_side_expression(disease_code, 'cases_nv_measles'))

    post_validation_rule(rule_id=rule_id,
                         rule_name='Sarampo case in a district a month',
                         rule_description='5 cases in a district in a month',
                         rule_instruction='5 cases in a district in a month',
                         organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('district')),
                         left_side_expression=left_side_expression,
                         left_side_description='Sarampo cases in recent EPI weeks',
                         date_element_ids=date_element_ids,
                         right_side_expression='0',
                         additional_rule_type=ADDITIONAL_RULE_TYPE.SarampoCaseInMonths,
                         additional_rule='A:4\r\nB:5'
                         )


def post_all_validation_groups():
    user_groups = get_user_groups().json().get('userGroups')
    user_group = user_groups[0].get('id')

    for rule_id in VALIDATION_RULE_GROUP:
        group_id = VALIDATION_RULE_GROUP.get(rule_id).get('group_id')
        name = VALIDATION_RULE_GROUP.get(rule_id).get('name')
        post_validation_rule_group(group_id=group_id, name=name, validation_rule_id=rule_id, user_group=user_group)


def post_all_validation_rules():
    add_colera_case()
    add_colera_deth()
    add_diarreia_death()
    add_disenteria_case()
    add_peste_case()
    add_pfa_case()
    add_raiva_case()
    add_raiva_death()
    add_sarampo_case()
    add_tetanus_case()

    add_malaria_case()
    add_complex_disenteria_case()
    add_complex_sarampo_case()
    add_meningite_case()
