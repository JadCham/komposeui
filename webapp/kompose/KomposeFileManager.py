import os
import uuid
import zipfile
import shutil
from os.path import basename
import logging

# Get logger instance
logger = logging.getLogger('kompose_logger')


class KomposeFileManager:

    def __init__(self, data_store_path="media/uploads/docker-compose/", zip_store_path="media/uploads/output/"):

        # Default storage paths
        self.data_store_path = data_store_path
        self.zip_store_path = zip_store_path

    def write_yaml_to_file(self, docker_compose_yaml):

        """
            Writes docker compose YAML to file and Returns absolute path
        """

        # Format docker compose file name
        docker_compose_file_path = "%s.yaml" % (self.generate_path())

        logger.debug("Writing docker compose to : %s" % docker_compose_file_path)

        # Write docker compose to file
        docker_compose_file = open(os.path.join(docker_compose_file_path), 'w')
        docker_compose_file.write(docker_compose_yaml)
        docker_compose_file.close()

        return os.path.abspath(docker_compose_file_path)

    def get_folder_path(self, docker_compose_yaml):

        """
        Returns docker compose path
        """

        # handle situation where zip_store_path doesnt exists
        if not os.path.isdir(self.zip_store_path):
            os.makedirs(self.zip_store_path)

        # Generate and create directory
        generated_folder_path = self.generate_path()
        os.makedirs(generated_folder_path)

        logger.debug("Created folder : %s" % generated_folder_path)

        # Format conversion store path
        self.data_store_path = "%s/" % generated_folder_path

        # Write input YAML to file and get path
        docker_compose_path = self.write_yaml_to_file(docker_compose_yaml)

        return docker_compose_path

    def get_zip_file_path(self):

        """
        Zip files in a directory and return zip file path
        :param upload: Pass django input

        """

        # Format zip file path
        zip_file_path = "%s%s.zip" % (self.zip_store_path, str(uuid.uuid4()))

        # Open zip file
        zipf = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

        # Loop over converted file in directory and add them to zip
        for root, dirs, files in os.walk(self.data_store_path):
            for file in files:
                zipf.write(os.path.join(root, file), basename(os.path.join(root, file)))

        # Close file
        zipf.close()

        logger.debug("Zip file created : %s" % zip_file_path)

        return zip_file_path

    def generate_path(self):

        # handle situation where data_store_path doesnt exists
        if not os.path.isdir(self.data_store_path):
            os.makedirs(self.data_store_path)

        generated_path = "%s%s" % (self.data_store_path, str(uuid.uuid4()))
        return generated_path

    def cleanup_docker_compose_path(self, generated_path):

        """
        Delete created file
        :param generated_path: Previously generated path

        """

        os.remove(generated_path)
        logger.debug("Removed file : %s" % generated_path)

    def cleanup_yaml_folder_path(self):

        """
        Delete folder containing converted yaml files
        """

        shutil.rmtree(self.data_store_path)
        logger.debug("Removed folder : %s" % self.data_store_path)

