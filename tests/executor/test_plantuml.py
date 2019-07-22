# pylint: disable=missing-docstring
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock, ANY

import pytest

from muextensions.executor import ExecutionError
from muextensions.connector.docutils.plantuml import PlantUmlWrapper


@pytest.mark.parametrize('output_format', ('lkj', '', '0', 'gif', None))
def test_init_bad_output_format(output_format):
    with pytest.raises(ValueError):
        PlantUmlWrapper('dummy data', output_format)


@pytest.mark.parametrize('output_format', ('png', 'svg'))
def test_init_good_output_format(output_format):
    PlantUmlWrapper('dummy data', output_format)


@pytest.mark.parametrize('uml_body', (None, 0, 1, 1000))
def test_init_bad_uml_body(uml_body):
    with pytest.raises(TypeError):
        PlantUmlWrapper(uml_body)


@pytest.mark.parametrize('uml_body, expected', (
    ('aslkj', '72358c47e4d989513974b4af3dbe5688'),
    ('some\nmulti\nline', 'c2057136edf6078533220334df0892e4'),
))
def test_hashcode(uml_body, expected):
    assert PlantUmlWrapper(uml_body).hashcode() == expected


@pytest.mark.parametrize('output_format', ('png', 'svg'))
@patch('muextensions.executor.plantuml.execute')
def test_write_happy_test(execute_mock, output_format):
    # Arrange
    extension = '.{}'.format(output_format)
    type(execute_mock).side_effect = MagicMock(
        side_effect=lambda cmd: cmd[2].with_suffix(extension).touch())
    # Apply
    with TemporaryDirectory() as temp_dir:
        target_file = Path(temp_dir, 'some-test-file').with_suffix(extension)
        PlantUmlWrapper('hello there', output_format).write(target_file)
    # Assert
    execute_mock.assert_called_with(
        ['plantuml', '-t{}'.format(output_format), ANY])


@patch('muextensions.executor.plantuml.execute')
def test_write_failed_write(execute_mock):
    # Arrange
    target_file = Path('/some/file/some-test-file.svg')
    with pytest.raises(ExecutionError):
        PlantUmlWrapper('hello there').write(target_file)
    execute_mock.assert_called_with(['plantuml', '-tsvg', ANY])
