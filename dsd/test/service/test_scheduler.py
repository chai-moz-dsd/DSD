from unittest import TestCase
from unittest.mock import patch


class SchedulerTest(TestCase):
    @patch('dsd.service.scheduler.pull_data')
    def test_should_periodically_execute_task(self, pull_data):
        pull_data.return_value = None
        pull_data()
        self.assertEqual(1, 2)
