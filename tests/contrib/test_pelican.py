from pathlib import Path
from unittest.mock import patch, sentinel

from muextensions.contrib import pelican


@patch('muextensions.contrib.pelican.ditaa')
@patch('muextensions.contrib.pelican.plantuml')
def test_pelican_init(plantuml_mock, ditaa_mock):
    pelican_obj = sentinel.pelican_obj
    pelican_obj.settings = {'OUTPUT_PATH': 'some/target/path'}

    pelican.pelican_init(pelican_obj)

    plantuml_mock.register.assert_called_once_with(
        target_dir=Path('some/target/path/images/_generated'),
        base_uri='/images/_generated',
        create_dir=True)
    ditaa_mock.register.assert_called_once_with(
        target_dir=Path('some/target/path/images/_generated'),
        base_uri='/images/_generated',
        create_dir=True)


@patch('muextensions.contrib.pelican.signals')
def test_register(signals_mock):
    pelican.register()
    signals_mock.initialized.connect.assert_called_with(pelican.pelican_init)
