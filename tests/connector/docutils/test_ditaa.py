from pathlib import Path
from unittest.mock import patch, sentinel, MagicMock
import pytest
from bs4 import BeautifulSoup

from docutils.core import publish_file
from docutils.parsers.rst.directives.images import Image

from muextensions.connector.docutils import ditaa

from ...testhelper import preserve_docutils_directives


RESOURCES_DIR = Path(__file__).with_suffix('')
REST_SAMPLE_FILE = RESOURCES_DIR / 'sample-default.rst'


# -----------------------------------------------------------------------------
# register()
# -----------------------------------------------------------------------------
@patch('muextensions.connector.docutils.ditaa.register_directive')
@patch('muextensions.connector.docutils.ditaa.build_ditaa_image_directive')
def test_register_defaults(build_mock, register_directive_mock, tmp_path):
    # pylint: disable=protected-access
    type(build_mock).return_value = sentinel.clazz
    ditaa.register(tmp_path)
    build_mock.assert_called_once_with(tmp_path, None, 'png', False)
    register_directive_mock.assert_called_once_with(
        'ditaa-image', sentinel.clazz)


@patch('muextensions.connector.docutils.ditaa.register_directive')
@patch('muextensions.connector.docutils.ditaa.build_ditaa_image_directive')
def test_register_modified(build_mock, register_directive_mock, tmp_path):
    type(build_mock).return_value = sentinel.clazz
    ditaa.register(tmp_path, 'some/base/uri', 'svg', True)
    build_mock.assert_called_once_with(tmp_path, 'some/base/uri', 'svg', True)
    register_directive_mock.assert_called_once_with(
        'ditaa-image', sentinel.clazz)


# -----------------------------------------------------------------------------
# build_ditaa_image_directive()
# -----------------------------------------------------------------------------
def test_build_ditaa_image_directive():
    # pylint: disable=protected-access
    clazz = ditaa.build_ditaa_image_directive(
        sentinel.target_dir, sentinel.base_uri, sentinel.default_image_format,
        sentinel.create_dir)
    assert issubclass(clazz, Image)
    assert clazz.__module__ == 'muextensions.connector.docutils.ditaa'
    assert clazz.__name__ == 'DitaaImageDirective'
    assert clazz._target_dir is sentinel.target_dir
    assert clazz._base_uri is sentinel.base_uri
    assert clazz._default_image_format is sentinel.default_image_format
    assert clazz._create_dirs is sentinel.create_dir


# -----------------------------------------------------------------------------
# DitaaImageDirectiveBase.run()
# -----------------------------------------------------------------------------
@preserve_docutils_directives
@pytest.mark.parametrize('image_format', ('png', 'svg'))
def test_image_directive_run_baseline(
        ditaa_wrapper_class_mock, image_format, integration_output_path):
    # pylint: disable=redefined-outer-name
    # arrange
    ditaa.register(integration_output_path, default_image_format=image_format)
    output = integration_output_path.joinpath('sample.html')
    # apply
    publish_file(source_path=str(REST_SAMPLE_FILE),
                 destination_path=str(output),
                 writer_name='html5')
    # assert
    expected_path = integration_output_path \
        .joinpath('fake_hash_code').with_suffix('.' + image_format)
    ditaa_wrapper_class_mock.instantiated_obj_mock \
        .write.assert_called_once_with(expected_path)
    with output.open(encoding='utf8') as data:
        soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    assert len(images) == 1
    assert images[0]['alt'] == images[0]['src']
    assert Path(images[0]['src']).suffix == '.' + image_format
    assert str(Path(images[0]['src']).parent) == str(integration_output_path)


@preserve_docutils_directives
def test_image_directive_run_default_base_uri(
        ditaa_wrapper_class_mock, integration_output_path):
    # pylint: disable=redefined-outer-name,unused-argument
    ditaa.register(integration_output_path, '.')
    output = integration_output_path.joinpath('sample.html')
    publish_file(source_path=str(REST_SAMPLE_FILE),
                 destination_path=str(output),
                 writer_name='html5')
    with output.open(encoding='utf8') as data:
        soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    assert images[0]['src'] == './fake_hash_code.png'


@preserve_docutils_directives
def test_image_directive_run_custom_base_uri(
        ditaa_wrapper_class_mock, integration_output_path):
    # pylint: disable=redefined-outer-name,unused-argument
    base_uri = './some/dir'
    images_path = integration_output_path.joinpath(base_uri)
    ditaa.register(images_path, base_uri, create_dir=True)
    html_output = integration_output_path.joinpath('sample.html')
    publish_file(source_path=str(REST_SAMPLE_FILE),
                 destination_path=str(html_output),
                 writer_name='html5')
    with html_output.open(encoding='utf8') as data:
        soup = BeautifulSoup(data, 'html.parser')
    images = soup.find_all('img')
    assert images[0]['src'] == './some/dir/fake_hash_code.png'


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def ditaa_wrapper_class_mock():
    # arrange
    with patch('muextensions.connector.docutils.ditaa.DitaaWrapper') as clazz:
        obj_mock = MagicMock()
        obj_mock.hashcode.return_value = 'fake_hash_code'
        type(clazz).return_value = obj_mock
        clazz.instantiated_obj_mock = obj_mock
        yield clazz
