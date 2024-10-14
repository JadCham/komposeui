from webapp.kompose import KomposeWrapper
from webapp.kompose.KomposeExceptions.KomposeConvertException import KomposeConvertException
from webapp.kompose.KomposeFileManager import KomposeFileManager
import unittest
import yaml
import os

class TestKomposeWrapper(unittest.TestCase):

    def setUp(self):

        self.kompose_file_manager = KomposeFileManager()

        with open("tests/resources/docker-compose.yaml", 'r') as docker_compose_file:
            self.docker_compose_yaml = docker_compose_file.read()

    def test_convert_web(self):
        docker_compose_path = self.kompose_file_manager.write_yaml_to_file(self.docker_compose_yaml)
        output, kubernetes_yaml = KomposeWrapper.kompose_convert_web(docker_compose_path, self.kompose_file_manager)

        parsed_kubernetes_yaml = list(yaml.load_all(kubernetes_yaml, Loader=yaml.SafeLoader))
        kompose_cmd = parsed_kubernetes_yaml[0]['metadata']['annotations']['kompose.cmd']
        kompose_version = parsed_kubernetes_yaml[0]['metadata']['annotations']['kompose.version']

        with open("tests/resources/output-k8s.yaml", 'r') as kubernetes_expected_file:
            # Replace kompose.version and kompose.cmd to match converted yaml
            expected_yaml = kubernetes_expected_file.read().replace("%VERSION%", kompose_version).replace("%CMD%",
                                                                                                          kompose_cmd)
            parsed_expected_yaml = list(yaml.load_all(expected_yaml, Loader=yaml.SafeLoader))

            self.assertEqual(parsed_expected_yaml, parsed_kubernetes_yaml)
    def test_kompose_exception_wrong_path(self):
        with self.assertRaises(KomposeConvertException):
            KomposeWrapper.kompose_convert_web("wrong_path", self.kompose_file_manager)
