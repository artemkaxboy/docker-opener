import pytest

from conftest import wait_for_container, get_container_logs

help_commands = ['h', '-h', 'help', '--help']


@pytest.mark.parametrize('command', help_commands)
def test_help_with_help_commands(no_args_image, command):
    status, container = wait_for_container(no_args_image, command)

    assert status['StatusCode'] == 0, "Container exited with non-zero status"

    logs = get_container_logs(container)

    assert "Usage:" in logs
    assert "Commands:" in logs
    assert "https://github.com/artemkaxboy/docker-opener" in logs
