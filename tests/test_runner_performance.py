import unittest

from orbeon_xml_api.builder import Builder
from orbeon_xml_api.runner import Runner
from orbeon_xml_api.utils import xml_from_file


class RunnerTestCase(unittest.TestCase):

    def setUp(self):
        super(RunnerTestCase, self).setUp()

        self.runner_xml = xml_from_file('tests/data', 'test_controls_runner.xml')
        self.builder_xml = xml_from_file('tests/data', 'test_controls_builder.xml')
        self.builder = Builder(self.builder_xml)

    # TODO remove this from API support?
    # Too slow
    def test_performance_10_builder_xml(self):
        for i in range(1, 10):
            Runner(self.runner_xml, None, self.builder_xml)

    def test_performance_100_builder_xml(self):
        for i in range(1, 100):
            Runner(self.runner_xml, None, self.builder_xml)

    def test_performance_1000_builder_xml(self):
        for i in range(1, 1000):
            Runner(self.runner_xml, None, self.builder_xml)

    # Fast enough ;)
    def test_performance_10_builder(self):
        for i in range(1, 10):
            Runner(self.runner_xml, self.builder)

    def test_performance_100_builder(self):
        for i in range(1, 100):
            Runner(self.runner_xml, self.builder)

    def test_performance_1000_builder(self):
        for i in range(1, 1000):
            Runner(self.runner_xml, self.builder)
