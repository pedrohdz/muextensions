import datetime
import re
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).with_name('helper')))

OUTPUT_DIR_OPTION = '--save-integration-output-to'
RUN_INTEGRATION_OPTION = '--run-integration'


def pytest_addoption(parser):
    parser.addoption(
        RUN_INTEGRATION_OPTION,
        action='store_true',
        default=False,
        help=('Run integration tests. Requires Ditaa and PlantUML to be '
              'installed.')
    )
    parser.addoption(
        OUTPUT_DIR_OPTION,
        action='store',
        default=None,
        help=('Directory to save files created by integration tests. The '
              'directory will be created if it does not already exist. '
              'Delete the directory between runs to avoid errors.')
    )


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'integration: mark test requiring Ditaa and PlantUML')


def pytest_collection_modifyitems(config, items):
    if config.getoption(RUN_INTEGRATION_OPTION):
        # Do not skip integration tests.
        return
    skip_slow = pytest.mark.skip(
        reason='needs {} option to run'.format(RUN_INTEGRATION_OPTION))
    for item in items:
        if 'integration' in item.keywords:
            item.add_marker(skip_slow)


RUN_DATETIME = datetime.datetime.now().isoformat()


@pytest.fixture
def integration_output_path(request, pytestconfig, tmp_path):
    value = pytestconfig.getoption(OUTPUT_DIR_OPTION)
    if not value:
        return tmp_path

    # We don't want to create everything, just the top two directories.
    base_path = Path(value, RUN_DATETIME)
    base_path.parent.mkdir(exist_ok=True)
    base_path.mkdir(exist_ok=True)

    base_path = base_path.resolve()
    directory = '+'.join([
        request.node.module.__name__,
        request.node.name])
    directory = re.sub(r'[^\w\+]', '_', directory)
    dir_path = base_path / directory
    dir_path.mkdir(exist_ok=False)
    return dir_path
