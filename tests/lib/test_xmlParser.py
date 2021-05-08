import pytest
from unittest.mock import patch
from xml.etree.cElementTree import Element, SubElement
from lib.XmlParser import XmlParser
from collections import defaultdict
from lib.IotError import XmlParserError

class TestXmlParser:

	def test_root_child_elements_successfully(self):
		with patch('xml.etree.ElementTree.fromstring') as mock_element_tree:
			# GIVEN
			# Create return value for the fromstring method
			root_element = Element('root')
			child_element = SubElement(root_element, 'child1')
			child_element.tag = 'child1'
			child_element.text = 'text1'
			mock_element_tree.return_value = root_element

			# Input XML that is going to be processed
			xml = '<root><child1>text1</child1></root>'

			# Expected dictionary with elements
			expected_elements = defaultdict(str)
			expected_elements['child1'] = 'text1'

			# WHEN
			xml_parser = XmlParser()
			elements = xml_parser.parse_root_child_elements_into_dictionary(xml)

			# THEN
			assert elements == expected_elements
			mock_element_tree.assert_called_once_with(xml)
