import logging

from dsd.models import Province
from dsd.models.remote.province import Province as ProvinceRemote

logger = logging.getLogger(__name__)


def pull_data():
    logger.info("remote province count = %s" % ProvinceRemote.objects.count())
    logger.info("remote province count = %s" % Province.objects.count())
