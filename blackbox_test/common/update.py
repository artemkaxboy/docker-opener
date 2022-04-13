import pytest

from conftest import wait_for_container, get_container_logs

# update_commands = ['u', 'update'] # FIXME - does not work for second update
update_commands = ['u']


@pytest.mark.parametrize('command', update_commands)
def test_update_with_no_image(no_args_image_for_function, command):
    status, container = wait_for_container(no_args_image_for_function, command)

    assert status['StatusCode'] == 0, "Container exited with non-zero status"

    logs = get_container_logs(container)

    assert "Pulling" in logs
    assert "OK" in logs
