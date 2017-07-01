from . import CommonTestCase

from orbeon_xml_api.controls import StringControl


class InputCounterTestCase(CommonTestCase):

    def setUp(self):
        super(InputCounterTestCase, self).setUp()
        self.control = self.builder.controls['input-counter']

    def test_control(self):
        self.assertIsInstance(self.control, StringControl)

    def test_builder_bind(self):
        self.assertEqual(self.control.bind.id, 'input-counter-bind')
        self.assertEqual(self.control.bind.name, 'input-counter')

    def test_builder_form(self):
        self.assertEqual(self.control.label, 'Input Field with Character Counter')
        self.assertEqual(self.control.alert, '30 characters maximum')
        self.assertEqual(self.control.hint, None)

        self.assertEqual(self.control.element.label, 'Input Field with Character Counter')
        self.assertEqual(self.control.element.alert, '30 characters maximum')
        self.assertEqual(self.control.element.hint, None)

    def test_builder_form_default_value(self):
        self.assertEqual(self.control.default_raw_value, 'This must not be "too long"!')
        self.assertEqual(self.control.default_value, 'This must not be "too long"!')

    def test_runner_input_counter(self):
        text = "Don't even try to make it too long!"
        self.assertEqual(self.runner.get_value('input-counter'), text)
        self.assertEqual(self.runner.form.inputcounter, text)
