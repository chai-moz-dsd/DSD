import logging

from django.core.exceptions import ObjectDoesNotExist

from dsd.models import District
from dsd.models.remote.district import District as DistrictRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync_district():
    all_remote_districts = DistrictRemote.objects.all()
    all_local_districts = get_all_local_districts(all_remote_districts)
    all_valid_local_districts = filter(is_valid_district, all_local_districts)

    save_districts(all_valid_local_districts)


def is_valid_district(district):
    if not district.district_name:
        return False
    return True


def get_all_local_districts(all_remote_districts):
    all_local_districts = []
    for remote_district in all_remote_districts:
        remote_district.__dict__.pop('_state')
        local_district = District(**remote_district.__dict__)
        local_district.uid = id_generator.generate_id()
        all_local_districts.append(local_district)

    return all_local_districts


def save_districts(districts):
    for district in districts:
        try:
            existing_district = District.objects.get(district_name=district.district_name)
            district.id = existing_district.id
            district.uid = existing_district.uid
        except ObjectDoesNotExist:
            pass
        finally:
            district.save()
