import logging

from dsd.models import District
from dsd.models.remote.district import District as DistrictRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync():
    all_remote_districts = DistrictRemote.objects.all()
    all_local_districts = get_all_local_districts(all_remote_districts)
    all_valid_local_districts = list(filter(is_valid_district, all_local_districts))

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
        local_district.uid = id_generator.generate_md5_id(local_district.district_name)
        all_local_districts.append(local_district)

    return all_local_districts


def save_districts(districts):
    for district in districts:
        filter_result = District.objects.filter(id=district.id)
        if not filter_result.count():
            district.save()
            continue

        if is_updated(district):
            existing_district = District.objects.get(id=district.id)
            district.id = existing_district.id
            district.province = existing_district.province
            district.uid = existing_district.uid
            district.save()


def is_updated(district_remote):
    district = District.objects.get(id=district_remote.id)
    return district_remote.district_name != district.district_name or \
           district_remote.description != district.description or \
           district_remote.data_creation != district.data_creation or \
           district_remote.user_creation != district.user_creation or \
           district_remote.state != district.state
