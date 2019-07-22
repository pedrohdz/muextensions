# pylint: disable=missing-docstring
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from muextensions import executor


@pytest.fixture
def process_mock():
    result = MagicMock()
    result.returncode = 0
    result.communicate = MagicMock(
        return_value=('Some STDOUT', 'Some STDERR'))
    return result


@patch('muextensions.executor.subprocess.Popen')
def test_happy_case(popen_mock, process_mock):
    # pylint: disable=redefined-outer-name
    popen_mock.configure_mock(return_value=process_mock)
    executor.execute('fake_command')
    process_mock.kill.assert_not_called()


@patch('muextensions.executor.subprocess.Popen')
def test_execute_timeout(popen_mock, process_mock):
    # pylint: disable=redefined-outer-name
    side_effects = (
        subprocess.TimeoutExpired('command', 30),
        ('Other STDOUT', 'Other STDERR'))
    process_mock.communicate = MagicMock(side_effect=side_effects)
    popen_mock.configure_mock(return_value=process_mock)

    with pytest.raises(executor.Timeout):
        executor.execute('command')
    process_mock.kill.assert_called_with()


@patch('muextensions.executor.subprocess.Popen')
def test_execute_subprocess_error(popen_mock, process_mock):
    # pylint: disable=redefined-outer-name
    side_effects = (
        subprocess.SubprocessError('command', 30),
        ('Other STDOUT', 'Other STDERR'))
    process_mock.communicate = MagicMock(side_effect=side_effects)
    popen_mock.configure_mock(return_value=process_mock)

    with pytest.raises(executor.ExecutionError):
        executor.execute('command')
    process_mock.kill.assert_called_with()


@patch('muextensions.executor.subprocess.Popen')
def test_execute_bad_returncode(popen_mock, process_mock):
    # pylint: disable=redefined-outer-name
    process_mock.returncode = 1
    popen_mock.configure_mock(return_value=process_mock)

    with pytest.raises(executor.ExecutionError):
        executor.execute('command')
