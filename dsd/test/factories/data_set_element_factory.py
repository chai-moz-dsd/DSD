import uuid
from datetime import datetime

import factory

from dsd.models import DataSetElement


class DataSetElementFactory(factory.DjangoModelFactory):
    class Meta:
        model = DataSetElement

    uid = uuid.uuid4()
    data_set_id = uuid.uuid4()
    complete_data = datetime.today()
    value = ''
    organization_unit_uid = uuid.uuid4()
