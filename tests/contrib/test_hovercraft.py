# import pytest
from unittest.mock import MagicMock, PropertyMock, patch

from muextentions.contrib import hovercraft


@patch('muextentions.contrib.hovercraft.plantuml')
def test_register(plantuml_mock):
    args = MagicMock()
    type(args).targetdir = PropertyMock(return_value='some/path/here')

    hovercraft.register(args)

    plantuml_mock.register.assert_called_with(
        'some/path/here/_generated', '_generated', True)