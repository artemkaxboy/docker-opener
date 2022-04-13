import pytest

from conftest import wait_for_container, get_container_logs

version_commands = ['v', '-v', 'version', '--version']


@pytest.mark.parametrize('command', version_commands)
def test_version(no_args_image, command):
    status, container = wait_for_container(no_args_image, command)

    assert status['StatusCode'] == 0, "Container exited with non-zero status"

    logs = get_container_logs(container)

    assert "Version: SNAPSHOT" in logs
    assert "Revision: LOCAL" in logs
    assert "Created: " in logs
