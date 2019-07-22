# pylint: disable=missing-docstring

import logging
import subprocess


LOG = logging.getLogger(__name__)


class ExecutionError(Exception):
    pass


class Timeout(ExecutionError):
    pass


def execute(command, timeout=30):
    try:
        LOG.debug('Executinge "%s".', command)
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_process(process)
        raise Timeout('Call to PlantUML took too long')
    except subprocess.SubprocessError:
        _kill_process(process)
        raise ExecutionError('Call to PlantUML failed with an exception')
    if process.returncode != 0:
        _log_process_failed(process, stdout, stderr)
        raise ExecutionError('Call to PlantUML failed')
    _log_process_sucess(process, stdout, stderr)


def _log_process_sucess(process, stdout, stderr):
    _log_process(True, process, stdout, stderr)


def _log_process_failed(process, stdout, stderr):
    _log_process(False, process, stdout, stderr)


def _kill_process(process):
    process.kill()
    stdout, stderr = process.communicate()
    _log_process_failed(process, stdout, stderr)


def _log_process(success, process, stdout, stderr):
    comment = 'succeeded' if success else 'failed'
    if success:
        comment = 'succeeded'
        level = logging.DEBUG
    else:
        comment = 'failed'
        level = logging.ERROR
    LOG.log(level, 'Command "%s" %s with a return code of "%d". '
            'STDOUT: %s STDERR: %s',
            process.args, comment, process.returncode, stdout, stderr)
