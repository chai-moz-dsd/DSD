import json
import logging
import time

from dsd.config import dhis2_config
from dsd.models import District
from dsd.models.remote.historical_data import HistoricalData as HistoricalDataRemote
from dsd.models import HistoricalCOCRelation
from datetime import date, timedelta

from dsd.repositories import dhis2_remote_repository

logger = logging.getLogger(__name__)


def get_all_historical_data():
    return HistoricalDataRemote.objects.all()


def build_historical_data_element_values_request_body_as_dict(historical_data_element_value):
    data_values = []
    historical_coc_relation = HistoricalCOCRelation.objects.filter(
        disease_id=historical_data_element_value.disease_id).first()
    data_values.append({
        'dataElement': historical_coc_relation.disease_uid,
        'value': historical_data_element_value.cases,
        'categoryOptionCombo': historical_coc_relation.cases_coc_id.coc_id
    })
    data_values.append({
        'dataElement': historical_coc_relation.disease_uid,
        'value': historical_data_element_value.deaths,
        'categoryOptionCombo': historical_coc_relation.deaths_coc_id.coc_id
    })
    start_week = "%sW%s" % (historical_data_element_value.year, historical_data_element_value.week)
    return {
        'dataSet': dhis2_config.DATA_SET_ID,
        'completeData': str(get_week_days(historical_data_element_value.year, historical_data_element_value.week)),
        'period': start_week,
        'orgUnit': District.objects.filter(id=historical_data_element_value.district_id).first().uid,
        'dataValues': data_values
    }


def post_historical_data_element_values(historical_data_element_values):
    for historical_data_element_value in historical_data_element_values:
        json_dumps = json.dumps(
            build_historical_data_element_values_request_body_as_dict(historical_data_element_value))
        dhis2_remote_repository.post_data_elements_value(json_dumps)


def post_historical_data_element_values_to_dhis2():
    logger.info('post historical data to DHIS2')
    historical_data_element_values = get_all_historical_data()
    post_historical_data_element_values(historical_data_element_values)
    time.sleep(5)
    dhis2_remote_repository.send_analysis_request()
    # Wait dhis2 finished data analysis
    time.sleep(10)


def get_week_days(year, week):
    d = date(year, 1, 1)
    d = d + timedelta(7 - d.weekday()) if d.weekday() > 3 else d - timedelta(d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt + timedelta(days=6)
