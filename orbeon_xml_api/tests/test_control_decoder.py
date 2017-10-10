import unittest
import xmltodict
from datetime import datetime, timedelta
from lxml import etree

from ..builder import Builder
from ..runner import Runner
from ..utils import xml_from_file


class StringDecoder(object):

    def __init__(self):
        self.username = 'novacode'
        self.api_token = 'abc123'

    def decode(self, value):
        new_value = "%s FROM StringDecoder" % value
        return new_value


class DateDecoder(object):

    def decode(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date() + timedelta(days=10)


class ImageAnnotationDecoder(object):

    def decode(self, value):
        res = {}

        if value is None:
            return res

        for el in value.getchildren():
            res[el.tag] = {el.tag: "%s FROM ImageAnnotationDecoder" % el.tag}

        return res


class AnyUriDecoderStaticImage(object):

    def decode(self, value):
        res = {'uri': None, 'value': None}

        if value is None:
            return res

        if isinstance(value, basestring):
            return {
                'uri': "%s BY THE %s" % (value, self.__class__.__name__),
                'value': "%s BY THE %s" % (value, self.__class__.__name__)
            }
        else:
            return {
                'uri': "%s BY THE %s" % (value.text, self.__class__.__name__),
                'value': "%s BY THE %s" % (value.text, self.__class__.__name__)
            }


class AnyUriDecoderImageAttachment(object):

    def decode(self, value):
        res = {'uri': None, 'value': None}

        if value is None:
            return res

        if isinstance(value, basestring):
            return {
                'uri': "%s FROM %s" % (value, self.__class__.__name__),
                'value': "%s FROM %s" % (value, self.__class__.__name__)
            }
        else:
            return {
                'uri': "%s FROM %s" % (value.text, self.__class__.__name__),
                'value': "%s FROM %s" % (value.text, self.__class__.__name__)
            }


class ControlDecoderTestCase(unittest.TestCase):

    def setUp(self):
        super(ControlDecoderTestCase, self).setUp()

        self.builder_xml = xml_from_file('tests/data', 'test_controls_builder_no-image-attachments-iteration.xml')
        self.runner_xml = xml_from_file('tests/data', 'test_controls_runner_no-image-attachments-iteration.xml')

    def test_simple_input_decoder(self):
        control_decoders = {
            'string': StringDecoder()
        }
        self.builder = Builder(self.builder_xml, 'en', control_decoders=control_decoders)
        self.runner = Runner(self.runner_xml, self.builder)

        self.assertEqual(self.runner.form.input.value, 'John FROM StringDecoder')

    def test_multiple_input_decoder(self):
        control_decoders = {
            'string': StringDecoder(),
            'date': DateDecoder()
        }
        self.builder = Builder(self.builder_xml, 'en', control_decoders=control_decoders)
        self.runner = Runner(self.runner_xml, self.builder)

        self.assertEqual(self.runner.form.input.value, 'John FROM StringDecoder')

        date_obj_add_10_days = datetime.strptime('2017-07-11', '%Y-%m-%d').date()
        self.assertEqual(self.runner.form.date.value, date_obj_add_10_days)

    def test_image_attachment_decoder(self):
        control_decoders = {
            'any_uri': AnyUriDecoderImageAttachment()
        }
        self.builder = Builder(self.builder_xml, 'en', control_decoders=control_decoders)
        self.runner = Runner(self.runner_xml, self.builder)

        expected = "%s FROM AnyUriDecoderImageAttachment" % '/fr/service/persistence/crud/orbeon/runner/data/24/43dbaabe1e3aa8862fd4de321b619709d62cc097.bin'

        self.assertEqual(self.runner.form.imageattachment.uri, expected)
        self.assertEqual(self.runner.form.imageattachment.value, expected)

    def test_static_image_decoder(self):
        control_decoders = {
            'any_uri': AnyUriDecoderStaticImage()
        }
        self.builder = Builder(self.builder_xml, 'en', control_decoders=control_decoders)
        self.runner = Runner(self.runner_xml, self.builder)

        expected = "%s BY THE AnyUriDecoderStaticImage" % '/fr/service/persistence/crud/orbeon/builder/data/33/a8523db8eba50aac53dfe15ece2758e6475cfc21.bin'

        self.assertEqual(self.runner.form.staticimage.uri, expected)
        self.assertEqual(self.runner.form.staticimage.value, expected)


    def test_image_annotation_decoder(self):
        control_decoders = {
            'image_annotation': ImageAnnotationDecoder()
        }
        self.builder = Builder(self.builder_xml, 'en', control_decoders=control_decoders)
        self.runner = Runner(self.runner_xml, self.builder)

        self.assertEqual(self.runner.form.imageannotation.image, 'image FROM ImageAnnotationDecoder')
        self.assertEqual(self.runner.form.imageannotation.annotation, 'annotation FROM ImageAnnotationDecoder')