from webapp.kompose import KomposeWrapper
from webapp.kompose.KomposeExceptions.KomposeConvertException import KomposeConvertException
from webapp.kompose.KomposeFileManager import KomposeFileManager
import unittest


class TestKomposeWrapper(unittest.TestCase):

    def setUp(self):

        self.kompose_file_manager = KomposeFileManager()

        with open("tests/resources/docker-compose.yaml", 'r') as docker_compose_file:
            self.docker_compose_yaml = docker_compose_file.read()

    def test_convert_web(self):
        docker_compose_path = self.kompose_file_manager.write_yaml_to_file(self.docker_compose_yaml)
        output, kubernetes_yaml = KomposeWrapper.kompose_convert_web(docker_compose_path, self.kompose_file_manager)

        with open("tests/resources/output-k8s.yaml", 'r') as kubernetes_expected_file:
            self.assertIn(kubernetes_expected_file.read(), kubernetes_yaml)

    def test_kompose_exception_wrong_path(self):
        with self.assertRaises(KomposeConvertException):
            KomposeWrapper.kompose_convert_web("wrong_path", self.kompose_file_manager)
