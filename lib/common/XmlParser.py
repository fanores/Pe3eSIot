"""XML Parser"""
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import ParseError
from collections import defaultdict
from lib.common.IotError import XmlParserError


class XmlParser:

    def parse_root_child_elements_into_dictionary(self, xml):
        """
            Parse XML
            Stores root's child XML elements into a dictionary.
        :return: dictionary of all child elements of the ROOT node
        """
        child_elements = defaultdict(str)

        try:
            root_element = ElementTree.fromstring(xml)
        except ParseError as error:
            raise XmlParserError(print(error))

        for child_element in root_element:
            child_elements[child_element.tag] = child_element.text

        return child_elements
