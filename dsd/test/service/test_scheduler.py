from unittest import TestCase
from unittest.mock import patch

from celery.schedules import crontab

from dsd.test.helper.mock_celery import MockPeriodicTask


class SchedulerTest(TestCase):
    @patch('dsd.service.scheduler.pull_data')
    def test_should_periodically_execute_task(self, pull_data):
        pull_data.return_value = None
        pull_data()
        MockPeriodicTask.assert_called_with(crontab())
