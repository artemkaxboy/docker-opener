import re
import socket

from docker.models.containers import Container
from docker.types import HostConfig
from docker.utils import utils

from errors import ObjectNotFoundError
from tools import docker_image_tools, docker_common_tools, system_tools
from tools.docker_common_tools import get_docker, get_docker_version
from tools.docker_image_tools import get_image_name

port_forward_entrypoint = "socat"


def get_container(container_id: str) -> Container:
    return get_docker().containers.get(container_id)


def stop_container(container_id: str):
    container: Container = get_container(container_id)
    print("Stopping `%s`" % container.name)
    container.stop()


def remove_container(container_id: str):
    container: Container = get_container(container_id)
    print("Deleting `%s`" % container.name)
    container.remove()


def rename_container(container_id: str, new_name: str):
    container: Container = get_container(container_id)
    print("Renaming container `%s` to `%s`" % (container.name, new_name))
    container.rename(new_name)


def start_container(container_id: str):
    container: Container = get_container(container_id)
    print("Starting `%s`" % container.name)
    container.start()
    print("Started `%s`" % container.name)


def copy_container(container_id: str, new_container_name: str = None) -> str:
    container = get_container(container_id)
    print("Copying container `%s` to " % container.name, end='')
    new_container_id = get_docker().api.create_container(image=docker_image_tools.get_image_name(container),
                                                         command=container.attrs['Config'].get('Cmd', None),
                                                         hostname=container.attrs['Config'].get('Hostname', None),
                                                         user=container.attrs['Config'].get('User', None),
                                                         ports=container.attrs['Config'].get('ExposedPorts', None),
                                                         environment=container.attrs['Config'].get('Env', None),
                                                         volumes=container.attrs['Config'].get('Volumes', None),
                                                         name=new_container_name,
                                                         entrypoint=container.attrs['Config'].get('Entrypoint', None),
                                                         working_dir=container.attrs['Config'].get('WorkingDir', None),
                                                         domainname=container.attrs['Config'].get('Domainname', None),
                                                         host_config=container.attrs.get('HostConfig', None),
                                                         mac_address=container.attrs['Config'].get('MacAddress', None),
                                                         labels=container.attrs['Config'].get('Labels', None),
                                                         stop_signal=container.attrs['Config'].get('StopSignal', None),
                                                         networking_config=container.attrs.get('NetworkSettings', None),
                                                         healthcheck=container.attrs['Config'].get('Healthcheck', None),
                                                         )
    print("`%s`" % get_container_name(new_container_id))
    return new_container_id


def open_port(target_id: str, host_port: int, target_port: int):
    """
    TODO fix
    Creates new container with bound host_port, connects new container to all networks which target container
    connected. New container forwards all traffic between opened host_port and target_port onto target_container
    bidirectionally.
    Port forwarding works until Ctrl+C pressed.
    :param target_id: target container identifier
    :param host_port: host port to bind
    :param target_port: target container port to open
    """
    target_container = get_container(target_id)
    print("Preparing port opener for `%s`" % target_container.name)

    opener_container_id = get_current_container_id()
    if opener_container_id is None:
        opener_image = "artemkaxboy/opener:snapshot"
    else:
        opener_image = get_image_name(opener_container_id)

    docker_version = get_docker_version()
    port_bindings = utils.convert_port_bindings({host_port: host_port})
    host_config = HostConfig(docker_version, port_bindings=port_bindings, auto_remove=True)

    new_container_id = get_docker().api.create_container(image=opener_image,
                                                         entrypoint=port_forward_entrypoint,
                                                         command=["TCP-LISTEN:%s,fork" % host_port,
                                                                  "TCP:%s:%s" % (
                                                                    get_container_ip(target_container), target_port)],
                                                         ports=[host_port],
                                                         host_config=host_config,
                                                         )
    port_opener_container = get_container(new_container_id)

    for network_name, network in target_container.attrs.get("NetworkSettings", {}).get("Networks", {}).items():
        get_docker().networks.get(network['NetworkID']).connect(new_container_id)

    start_container(new_container_id)
    try:
        print("Port opened: %s -> %s:%s" % (host_port, target_container.name, target_port))
        print("Press [Ctrl+C] to stop the app. Port will be closed automatically.")
        port_opener_container.wait()
    except KeyboardInterrupt:
        stop_container(new_container_id)


def get_container_name(container_id: str):
    """
    Finds container name.
    :param container_id: id of container to find name
    :return: found container name
    :raises ValueError if no container found
    """
    container: Container = get_container(container_id)
    return container.name


def find_container(target):
    """
    Finds one container by name, image, id or port.

    :param target: known container property
    :return: found container id
    :raises ObjectNotFoundError container is not found by given attribute or more than one container found
    """
    options = find_containers(target)

    if len(options) == 0:
        raise ObjectNotFoundError("Container `%s` not found!" % target)

    if len(options) != 1:
        docker_common_tools.docker_ps(list(map(lambda c: c.id, options)))
        raise ObjectNotFoundError("More than one container `%s` found!" % target)

    return options[0]


def find_container_id(target):
    """
    Finds one container's id by name, image, id or port.

    :param target: known attribute of wanted container
    :return: Found container's ID
    :raises ObjectNotFoundError if container not found or more than one container found
    """
    return find_container(target).id


def find_containers(target, raise_if_not_found=False, search_all=False):
    """
    Returns container by name, image, id, port.
    :param search_all: include stopped containers
    :param raise_if_not_found: raise error if no containers found
    :param target: known attribute of wanted container
    :return: Found container
    :raises ValueError if container not found
    """
    containers = get_docker().containers.list(all=search_all)

    container: Container
    found_containers = []
    for container in containers:
        if container.name == target:
            print("Found container with name `%s`" % target)
            return [container]

    for container in containers:
        if container.name.find(target) >= 0:
            print("Found container with name `%s` containing `%s`" %
                  (container.name, target))
            found_containers.append(container)
    if len(found_containers) > 0:
        return found_containers

    for container in containers:
        image_name = docker_image_tools.get_image_name(container)
        if image_name.find(target) >= 0:
            print("Found container with image `%s` containing `%s`" % (image_name, target))
            found_containers.append(container)
    if len(found_containers) > 0:
        return found_containers

    for container in containers:
        if container.id.find(target) >= 0:
            print("Found container with ID `%s` containing `%s`" % (container.id, target))
            found_containers.append(container)
    if len(found_containers) > 0:
        return found_containers

    for container in containers:
        if target in get_ports(container):
            print("Found container with exposed/mapped port `%s`" % target)
            found_containers.append(container)
    if len(found_containers) > 0:
        return found_containers

    if raise_if_not_found:
        raise ValueError("No containers found for `%s`!" % target)
    return found_containers


def find_container_ids(target: str, raise_if_not_found: bool = False, search_all: bool = False):
    return list(map(lambda c: c.id, find_containers(target, raise_if_not_found, search_all=search_all)))


def get_ports(container: Container):
    """
    Returns all exposed and mapped port of the given container as a set.
    :param container: to find port of.
    :return: set of ports
    """

    ports = set()

    for port in container.ports:
        # adds exposed port
        ports.add(port_to_string(port))

        # find mapped ports
        mapping = container.ports[port]
        found_ports = port_mapping_to_set(mapping)
        ports.update(found_ports)

    return ports


def port_mapping_to_set(raw_port):
    """
    Returns all mapped ports as a set.
    :param raw_port: port in any allowed format
        https://docker-py.readthedocs.io/en/stable/containers.html#container-objects.
    :return: set of ports
    """

    if raw_port is None:
        return set()

    raw_type = type(raw_port)

    if raw_type is int:
        return {str(raw_port)}

    if raw_type is dict:
        return {port_to_string(raw_port['HostPort'])}

    if raw_type is list:
        result = set()
        for element in raw_port:
            result.update(port_mapping_to_set(element))
        return result


def port_to_string(port):
    """
    Returns clear number string containing port number.
    :param port: port in integer (1234) or string ("1234/tcp") representation.
    :return: port number as number string ("1234")
    """
    port_type = type(port)
    if port_type is int:
        return str(port)
    if port_type is str:
        return re.findall(r"\d+", port)[0]


def docker_command(docker_command, args, allow_multiple_target=False, allow_options=True, require_command=False,
                   search_all=False, confirm_many=None):
    """
    Prepares command to fetch container logs.
    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    args1, command = system_tools.divide_options_and_command(args)
    if not require_command and len(command) > 0:
        raise ValueError("Command is not allowed")
    if require_command and len(command) < 1:
        raise ValueError("Command required")

    target, options = system_tools.divide_target_and_options(args1)
    if not allow_options and len(options) > 0:
        raise ValueError("Options are not allowed")
    if len(target) == 0:
        raise ValueError("Target required")

    target_ids = find_container_ids(target, search_all=search_all)
    if len(target_ids) == 0:
        raise ObjectNotFoundError("Container `%s` not found!" % target)

    if len(target_ids) > 1:
        if not allow_multiple_target:
            docker_common_tools.docker_ps(target_ids, search_all=search_all)
            raise ValueError("More than one container `%s` found!" % target)

        if confirm_many is not None:
            docker_common_tools.docker_ps(target_ids, search_all=search_all)
            if not system_tools.get_consent(confirm_many):
                exit(0)

    docker_common_tools.docker_ps(target_ids, search_all=search_all)

    to_run = "docker %s %s %s %s" % (docker_command, options, " ".join(target_ids), " ".join(command))
    print(to_run)
    system_tools.prepare_command(to_run)


def is_container_running(container: Container):
    """
    Checks if container running or not.
    :param container: container to check
    :return: true if running, false - otherwise
    """
    return container.attrs.get("State", {}).get("Running", False)


def is_container_autoremovable(container: Container):
    """
    Checks if container autoremovable (has option `--rm`) or not.
    :param container: container to check
    :return: true if autoremovable, false - otherwise
    """
    return container.attrs.get("HostConfig", {}).get("AutoRemove", False)


def get_current_container_id():
    """
    :return: current container id or None if id cannot be found
    """
    try:
        return find_container(socket.gethostname()).id
    except ObjectNotFoundError:
        return None


def get_container_ip(container: Container):
    """
    TODO fix
    :param container:
    :return:
    """
    for network_name, network in container.attrs.get("NetworkSettings", {}).get("Networks", {}).items():
        return network.get("IPAddress", None)
    return None
