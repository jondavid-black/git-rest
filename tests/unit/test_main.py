import sys
import types
import pytest
from unittest import mock

# Patch create_app to avoid running a real server
@mock.patch('git_rest.__main__.create_app')
def test_main_runs_with_defaults(mock_create_app):
    import git_rest.__main__ as main_mod
    mock_app = mock.Mock()
    mock_create_app.return_value = mock_app
    mock_app.run = mock.Mock()

    test_args = ['prog']
    with mock.patch.object(sys, 'argv', test_args):
        main_mod.main()
    mock_create_app.assert_called_once()
    mock_app.run.assert_called_once_with(host='0.0.0.0', port=5000)

@mock.patch('git_rest.__main__.create_app')
def test_main_runs_with_args(mock_create_app):
    import git_rest.__main__ as main_mod
    mock_app = mock.Mock()
    mock_create_app.return_value = mock_app
    mock_app.run = mock.Mock()

    test_args = ['prog', '--workdir', '/tmp', '--host', '127.0.0.1', '--port', '1234']
    with mock.patch.object(sys, 'argv', test_args):
        with mock.patch('os.chdir') as mock_chdir:
            main_mod.main()
            mock_chdir.assert_called_once_with('/tmp')
    mock_create_app.assert_called_once()
    mock_app.run.assert_called_once_with(host='127.0.0.1', port=1234)
