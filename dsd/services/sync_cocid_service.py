import json

import requests

from chai import settings
from dsd.config.dhis2_config import key_get_cocid
from dsd.models import CategoryCombination
from dsd.models import COCRelation
from dsd.repositories.dhis2_oauth_token import get_access_token


def get_category_combo_ids():
    category_combos = CategoryCombination.objects.all()
    ids = []
    for category_combo in category_combos:
        ids.append(category_combo.id)
    return ids


def get_category_option_combos(category_comb_id):
    url = key_get_cocid(category_comb_id)
    response = requests.get(url=url,
                            headers=oauth_header(),
                            verify=settings.DHIS2_SSL_VERIFY)
    return json.loads(response.text)


def update_coc_relation(cc_id, coc):
    coc_relation = COCRelation.objects.filter(cc_id=cc_id, name_of_coc=coc["name"]).first()
    coc_relation.coc_id = coc["id"]
    coc_relation.save()


def set_coc_id():
    cc_ids = get_category_combo_ids()
    for cc_id in cc_ids:
        res = get_category_option_combos(cc_id)["categoryOptionCombos"]
        for coc in res:
            update_coc_relation(cc_id, coc)


def oauth_header():
    return {'Authorization': 'bearer %s' % get_access_token()}
