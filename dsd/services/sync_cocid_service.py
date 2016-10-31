import json

import requests

from chai import settings
from dsd.config.dhis2_config import key_get_cocid
from dsd.models import CategoryCombination
from dsd.models import COCRelation
from dsd.models import HistoricalCOCRelation
from dsd.repositories.dhis2_remote_repository import PATH_TO_CERT


def get_category_combo_ids():
    return [category_combo.id for category_combo in CategoryCombination.objects.all()]


def get_category_option_combos(category_comb_id):
    url = key_get_cocid(category_comb_id)
    response = requests.get(url=url,
                            auth=(settings.USERNAME, settings.PASSWORD),
                            verify=PATH_TO_CERT)
    return json.loads(response.text)


def update_historical_coc_relation(coc_relation):
    historical_coc_relation = HistoricalCOCRelation.objects.filter(disease_uid=coc_relation)
    pass


def update_coc_relation(cc_id, coc):
    coc_relation = COCRelation.objects.filter(cc_id=cc_id, name_of_coc=coc["name"]).first()
    coc_relation.coc_id = coc["id"]
    coc_relation.save()
    update_historical_coc_relation(coc_relation)


def set_coc_id():
    cc_ids = get_category_combo_ids()
    for cc_id in cc_ids:
        res = get_category_option_combos(cc_id)["categoryOptionCombos"]
        for coc in res:
            update_coc_relation(cc_id, coc)
