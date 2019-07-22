from unittest.mock import patch, ANY

from muextensions.connector.docutils import plantuml


@patch('muextensions.connector.docutils.plantuml.directives')
def test_register_defaults(directives_mock):
    # pylint: disable=protected-access
    plantuml.register('a/target/directory')
    directives_mock.register_directive.assert_called_with('plantuml', ANY)
    directive_class = directives_mock.register_directive.call_args[0][1]
    assert directive_class._target_dir == 'a/target/directory'
    assert directive_class._base_uri is None
    assert not directive_class._create_dirs


@patch('muextensions.connector.docutils.plantuml.directives')
def test_register_custom_args(directives_mock):
    # pylint: disable=protected-access
    plantuml.register('another/target/directory', 'some/base', True)
    directive_class = directives_mock.register_directive.call_args[0][1]
    assert directive_class._target_dir == 'another/target/directory'
    assert directive_class._base_uri == 'some/base'
    assert directive_class._create_dirs


@patch('muextensions.connector.docutils.plantuml.directives')
def test_directive_defaults(directives_mock):
    # arrange
    plantuml.register('foo/bar')
    directive_class = directives_mock.register_directive.call_args[0][1]
    test_class = type('Foo', (directive_class,), {'__init__': lambda _: None})
    # act
    directive = test_class()
    # assert
    assert directive.target_dir == 'foo/bar'
    assert directive.base_uri is None
    assert not directive.create_dirs


@patch('muextensions.connector.docutils.plantuml.directives')
def test_directive_custom_args(directives_mock):
    # arrange
    plantuml.register('here/is/a/directory', 'a/base/2', True)
    directive_class = directives_mock.register_directive.call_args[0][1]
    test_class = type('Foo', (directive_class,), {'__init__': lambda _: None})
    # act
    directive = test_class()
    # assert
    assert directive.target_dir == 'here/is/a/directory'
    assert directive.base_uri == 'a/base/2'
    assert directive.create_dirs
