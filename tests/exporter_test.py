#!/usr/bin/python
# -*- coding: utf-8*-
"""

Tree Editor.
Copyright (C) 2014  ssimons

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""

import unittest
from src.modell.enumerations import CONFIG_ENUM
from tests.assistance.test_set import TestConfigurationSet
from src.modell.treestruct.tree_element import Tree
from src.modell.exporter import TextExporter

class ExporterTestWithoutData(unittest.TestCase):
    """Tests different tree structures using first, second and third delimiter.
    Test (tree -> text) is the reverse version of the Importer (text -> tree).
    """


    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_delimiter_test(self._conf)

    def test_proper_values_without_second_delimiter(self):
        """Tests the comparision of  proper values without second delimiter.
        """
        exporter = TextExporter(self._conf)

        first_child = self.test_set.should_tree.get_children()[0]
        str_represent = exporter.export_data_to_line(first_child)
        str_represent = str_represent.replace("\n", "")
        self.assertEquals(str_represent,
                          self.test_set.SAMPLE_LINE_SHORT,
                          "export result of should_tree compare not equal to"
                          + " SAMPLE_LINE_SHORT. " + str_represent + " vs. "
                          + self.test_set.SAMPLE_LINE_SHORT)

    def test_extracted_identifiers_incl_second_delimiter(self):
        """Tests the comparision of extracted identifiers including second
        delimiter"""

        self._change_second_delimiter(\
            self.test_set.EXISTING_SECOND_DELIMITER)
        exporter = TextExporter(self._conf)
        first_child = self.test_set. \
            should_tree_including_third_result.get_children()[0]
        str_represent = exporter.export_data_to_line(first_child)
        str_represent = str_represent.replace("\n", "")
        self.assertEquals(str_represent,
                          self.test_set.SAMPLE_LINE_FULL,
                          "Export result of should_tree_including_third_result"
                          + " using existing "
                          + "second delimiter not equal SAMPLE_LINE_FULL")

    def test_extracted_identifiers_incl_empty_str_2delimiter(self):
        """Tests the comparision of the extracted identifieres inclusive an
        empty string after the second delimiter.
        """
        self._change_second_delimiter(\
            self.test_set.EXISTING_SECOND_DELIMITER)
        exporter = TextExporter(self._conf)
        first_child \
 = self.test_set. \
            should_tree_without_3rd_result_but_2nd_delimiter. \
            get_children()[0]
        str_represent = exporter.export_data_to_line(first_child)
        str_represent = str_represent.replace("\n", "")
        self.assertEquals(str_represent,
            self.test_set. \
                SAMPLE_LINE_WITH_SECOND_DELIMITER_BUT_WITHOUT_THIRD_RESULT,
            "Export result of "
            + "should_tree_without_3rd_result_but_2nd_delimiter"
            + " using existing second delimiter not equal "
            + "SAMPLE_LINE_WITH_SECOND_DELIMITER_BUT_WITHOUT_THIRD_RESULT")


    def _change_second_delimiter(self, new_second_delimiter):
        self._conf.data[str(CONFIG_ENUM.SecondDelimiter)] \
 = new_second_delimiter

class ExporterTestCheckWithData(unittest.TestCase):
    """Tests different tree structures with data lines.
    Test (tree -> text) is the reverse version of the Importer (text -> tree).
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)
        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_test(self._conf)


    def test_proper_data_prefix_and_line(self):
        self._change_data_prefix(self.test_set.DATA_PREFIX_STAR)
        exporter = TextExporter(self._conf)
        first_child = self.test_set.should_tree_with_data.get_children()[0]
        str_represent = exporter.export_data_to_line(first_child)
        str_represent = str_represent.replace("\n", "")
        should_str = "".join([self.test_set.SAMPLE_LINE_SHORT, \
                              self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX]) \
                            .replace("\n", "")
        self.assertEquals(str_represent,
                          should_str,
                          "Export result of should_tree_with_data"
                          + " not equal SAMPLE_LINE_SHORT and "
                          + "SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX."
                          + str_represent + " vs. " + should_str)

    def _change_data_prefix(self, new_data_prefix):
        self._conf.data[str(CONFIG_ENUM.UseDataPrefix)] = True
        self._conf.data[str(CONFIG_ENUM.DataDelimiter)] \
 = new_data_prefix



class ExporterTestCheckInterpreteWithLineAsTreeElements(\
        unittest.TestCase):
    """Tests different tree structures with data lines as own tree elements
    (lowest level).
    Test (tree -> text) is the reverse version of the Importer (text -> tree).
    """
    def setUp(self):
        self._conf = TestConfigurationSet. \
            retrieve_test_configuration_data_as_treeelements()

        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_as_tree_elements_test(
            self._conf)


    def test_proper_data_prefix_and_line(self):
        exporter = TextExporter(self._conf)
        first_child = \
            self.test_set.should_tree_with_data_tree_elements.get_children()[0]
        str_represent = exporter.export_data_to_line(first_child)
        str_represent = str_represent.replace("\n", "")
        should_str = "".join([self.test_set.SAMPLE_LINE_SHORT, \
                              self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX]) \
                            .replace("\n", "")
        self.assertEquals(str_represent,
                          should_str,
                          "Export result of should_tree_with_data_tree_elements"
                          + " not equal SAMPLE_LINE_SHORT and "
                          + "SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX")
