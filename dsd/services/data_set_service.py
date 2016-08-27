import json
import logging

logger = logging.getLogger(__name__)


def build_data_set_element_request_body_as_json(data_set_element_list):
    if not len(data_set_element_list):
        return

    data_values = []
    for element in data_set_element_list:
        data_values.append({
            'dataElement': element.uid,
            'value': element.value
        })

    return json.dumps({
        "dataSet": data_set_element_list[0].data_set_id,
        "completeData": data_set_element_list[0].complete_data.strftime('%Y-%m-%d'),
        "period": data_set_element_list[0].complete_data.strftime('%Y%m'),
        "orgUnit": data_set_element_list[0].organization_unit_uid,
        "data_values": data_values
    })
