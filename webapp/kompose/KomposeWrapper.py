import os
import uuid
from subprocess import STDOUT, check_output, CalledProcessError
from webapp.kompose.KomposeExceptions.KomposeConvertException import KomposeConvertException
from webapp.ansi2html import *
import logging

# Get logger instance
logger = logging.getLogger('kompose_logger')


def kompose_convert_web(input_file_path, kompose_file_manager):
    """
    Returns converted docker compose in one file
    :param input_file_path: Docker compose file path
    :param kompose_file_manager: Manages the output storage

    Raises KomposeConvertException if something went wrong converting docker compose
    """
    try:

        # Get output file path
        output_file_path = kompose_file_manager.data_store_path + str(uuid.uuid4())

        # Format command to run in subprocess
        kompose_command = "kompose convert -f %s -o %s" % (input_file_path, output_file_path)

        logger.debug("Running kompose : %s" % kompose_command)

        # Run conversion and format shell output
        output = check_output(kompose_command, shell=True, stderr=STDOUT)
        output = "<br/>".join(output.decode("utf-8").split("\n"))
        output = ansi2html(output)

        # Read generated file
        f = open(output_file_path, 'r')
        kubernetes_yaml = f.read()
        f.close()

        # Cleanup file before returning YAML
        os.remove(output_file_path)

        # Return shell output and converted YAML tuple
        return output, kubernetes_yaml

    except CalledProcessError as e:

        logger.error('Something went wrong running kompose', exc_info=True)

        # Format and raise error
        error = "<br/>".join(e.output.decode("utf-8").split("\n"))
        raise KomposeConvertException(ansi2html(error))


def checkKomposeInstall():
    """
    Checks if kompose is installed by checking the version

    Raises KomposeConvertException if kompose not found
    """

    try:
        # Format command to run in subprocess
        kompose_command = "kompose version"

        # Run conversion and format shell output
        version = check_output(kompose_command, shell=True, stderr=STDOUT)

        logger.debug("Kompose version : %s" % version.decode("utf-8"))

    except CalledProcessError as e:

        logger.error("Kompose doesn't seem to be installed or not in correct path", exc_info=True)
        raise KomposeConvertException("Kompose doesn't seem to be installed or not in correct path")


def kompose_convert_multiple_files(input_file_path, kompose_file_manager):

    """
    Returns converted docker compose divided into files
    :param input_file_path: Docker compose file path
    :param kompose_file_manager: Manages the output storage

    Raises KomposeConvertException if something went wrong converting docker compose
    """
    try:

        # Format command to run in subprocess
        kompose_command = "kompose convert -f %s " % input_file_path

        # logger.debug("Running kompose : " % kompose_command)

        # Run conversion and format shell output
        output = check_output(kompose_command, shell=True, stderr=STDOUT, cwd=kompose_file_manager.data_store_path)
        output = "<br/>".join(output.decode("utf-8").split("\n"))
        output = ansi2html(output)

        # Delete docker compose
        kompose_file_manager.cleanup_docker_compose_path(input_file_path)

        # Return shell output
        return output

    except CalledProcessError as e:
        logger.error('Something went wrong running kompose', exc_info=True)

        # Format and raise error
        error = "<br/>".join(e.output.decode("utf-8").split("\n"))
        raise KomposeConvertException(ansi2html(error))

    except Exception as e:
        logger.error('Something went wrong running kompose', exc_info=True)

        # Format and raise error
        error = "<br/>".join(e.output.decode("utf-8").split("\n"))
        raise KomposeConvertException(ansi2html(error))
