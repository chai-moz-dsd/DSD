import uuid
from datetime import datetime

import factory

from dsd.models.sender_middleware_core import SenderMiddlewareCore


class SenderMiddlewareCoreFactory(factory.DjangoModelFactory):
    class Meta:
        model = SenderMiddlewareCore

    uri = 'uuid:%s' % uuid.uuid1()
    creator_uri_user = 'uid:maputo-manhica|%s' % datetime.today()
    creation_date = datetime.today()
    last_update_uri_user = None
    last_update_date = datetime.today()
    model_version = None
    ui_version = None
    is_complete = True
    submission_date = datetime.today()
    marked_as_complete_date = datetime.today()
    device_id_test_output = None
    end_test_output = None
    phone_number = None
    today = datetime.today()
    start_test_output = None
    sim_serial_test_output = None
    metadata_note = None
    note_intro = None
    note_description = None
    meta_instance_id = 'uuid:%s' % uuid.uuid4()
    sim_serial = factory.Iterator(
        ['8925801150348701867f', '8925801150348674270f', '8925801150348701842f', '8925801150348701768f',
         '8925801150348674791f'])
    device_id = factory.Iterator([356670060315512, 356670060310919, 356670060314465, 356670060310976])
    open_field = None
    phone_number_test_output = None
    start = datetime.today()
    end = datetime.today()
    today_test_output = None
