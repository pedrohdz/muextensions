from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

from muextensions.contrib import hovercraft


@patch('muextensions.contrib.hovercraft.ditaa')
@patch('muextensions.contrib.hovercraft.plantuml')
def test_register(plantuml_mock, ditaa_mock):
    args = MagicMock()
    type(args).targetdir = PropertyMock(return_value='some/path/here')

    hovercraft.register(args)

    plantuml_mock.register.assert_called_with(
        target_dir=Path('some/path/here/_generated'),
        base_uri='_generated',
        create_dir=True)
    ditaa_mock.register.assert_called_with(
        target_dir=Path('some/path/here/_generated'),
        base_uri='_generated',
        create_dir=True)
