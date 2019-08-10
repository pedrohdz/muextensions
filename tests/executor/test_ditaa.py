# pylint: disable=missing-docstring
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY
import pytest

from muextensions.executor.ditaa import DitaaWrapper


RESOURCES_DIR = Path(__file__).with_suffix('')
SAMPLE_DITAA_FILE = RESOURCES_DIR / 'sample.ditaa'


@pytest.fixture
def execute_mock():
    with patch('muextensions.executor.ditaa.execute') as mock:
        type(mock).side_effect = \
            MagicMock(side_effect=lambda _: Path(_[2]).touch())
        yield mock


@pytest.mark.parametrize('file,expected', (
    (RESOURCES_DIR/'sample.ditaa', '5848cd55fa649d0fadf0c243f890a305'),
))
def test_hashcode(file, expected):
    assert DitaaWrapper.from_file(file).hashcode() == expected


@pytest.mark.integration
@pytest.mark.parametrize('file', (SAMPLE_DITAA_FILE,))
def test_happy_svg_integration(file, integration_output_path):
    target = integration_output_path.joinpath(file.name).with_suffix('.svg')
    DitaaWrapper.from_file(file).write(target)
    assert target.exists()
    assert target.stat().st_size > 1000


@pytest.mark.integration
@pytest.mark.parametrize('file', (SAMPLE_DITAA_FILE,))
def test_happy_png_integration(file, integration_output_path):
    target = integration_output_path.joinpath(file.name).with_suffix('.png')
    DitaaWrapper.from_file(file, output_format='png').write(target)
    assert target.exists()
    assert target.stat().st_size > 1000


def test_write_with_svg(execute_mock, tmp_path):
    # pylint: disable=redefined-outer-name
    output = tmp_path.joinpath('nothing.svg')
    DitaaWrapper.from_file(SAMPLE_DITAA_FILE).write(output)
    assert '--svg' in execute_mock.call_args[0][0]
    assert output.exists()


def test_write_with_png(execute_mock, tmp_path):
    # pylint: disable=redefined-outer-name
    output = tmp_path.joinpath('nothing.png')
    DitaaWrapper.from_file(SAMPLE_DITAA_FILE, output_format='png') \
        .write(output)
    assert '--svg' not in execute_mock.call_args[0][0]
    assert output.exists()


@patch('muextensions.executor.ditaa.execute')
def test_write_failed_write(patched_execute, tmp_path):
    output = tmp_path.joinpath('nothing.svg')
    with pytest.raises(FileNotFoundError):
        DitaaWrapper.from_file(SAMPLE_DITAA_FILE).write(output)
    patched_execute.assert_any_call(ANY)
    assert not output.exists()


@pytest.mark.parametrize('ditaa_body', (1, None, True))
def test_init_bad_body(ditaa_body):
    with pytest.raises(TypeError):
        DitaaWrapper(ditaa_body)


@pytest.mark.parametrize('output_format', (1, None, True))
def test_init_bad_format(output_format):
    with pytest.raises(ValueError):
        DitaaWrapper(('one', 'two', 'three'), output_format=output_format)
