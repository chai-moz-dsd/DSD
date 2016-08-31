import logging

from django.core.exceptions import ObjectDoesNotExist

from dsd.models import Province
from dsd.models.remote.province import Province as ProvinceRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync(sync_time):
    if not sync_time:
        all_remote_provinces = ProvinceRemote.objects.all()
        logger.debug('sync all provinces from %s' % sync_time)
    else:
        all_remote_provinces = ProvinceRemote.objects.filter(created__gte=sync_time)
        logger.debug('sync provinces from %s' % sync_time)

    all_local_provinces = get_all_local_provinces(all_remote_provinces)
    all_valid_local_provinces = filter(is_valid_province, all_local_provinces)

    save_provinces(all_valid_local_provinces)


def is_valid_province(province):
    if not province.province_name:
        return False
    return True


def get_all_local_provinces(all_remote_provinces):
    all_local_provinces = []
    for remote_province in all_remote_provinces:
        remote_province.__dict__.pop('_state')
        local_province = Province(**remote_province.__dict__)
        local_province.uid = id_generator.generate_id()
        all_local_provinces.append(local_province)

    return all_local_provinces


def save_provinces(provinces):
    for province in provinces:
        try:
            existing_province = Province.objects.get(province_name=province.province_name)
            province.id = existing_province.id
            province.uid = existing_province.uid
        except ObjectDoesNotExist:
            pass
        finally:
            province.save()
