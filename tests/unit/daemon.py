import os
import mock
import inspect
from unittest import TestCase

import dvc.daemon as daemon


class TestDaemon(TestCase):
    @mock.patch('dvc.daemon._spawn_posix')
    @mock.patch('dvc.daemon._spawn_windows')
    def test(self, mock_windows, mock_posix):
        daemon.daemon(['updater'])

        if os.name == 'nt':
            mock_posix.assert_not_called()
            mock_windows.assert_called()
            args, kwargs = mock_windows.call_args
        else:
            mock_windows.assert_not_called()
            mock_posix.assert_called()
            args, kwargs = mock_posix.call_args

        env = args[1]
        self.assertTrue('PYTHONPATH' in env.keys())

        file_path = os.path.abspath(inspect.stack()[0][1])
        file_dir = os.path.dirname(file_path)
        test_dir = os.path.dirname(file_dir)
        dvc_dir = os.path.dirname(test_dir)
        self.assertEqual(env['PYTHONPATH'], dvc_dir)
