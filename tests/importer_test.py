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

import copy
from src.modell.enumerations import CONFIG_ENUM
from src.modell.importer import TextImporter
from tests.assistance.test_set import TestConfigurationSet
from src.modell.treestruct.tree_element import Tree
from src.modell import tree_operations
from src.modell.logger import logging
from tests.assistance.tree_test_base import TreeTestBase

class ImporterTestCheckInterpreteLineWithoutData(TreeTestBase):
    """Tests different tree structures using first, second and third delimiter.
    """


    def test_identifiers_without_second_delimiter(self):
        """
        Tests comparision of extracted identifiers without second delimiter
        """
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                                      self.tree_instance)
        self.assert_tree(self.tree_instance,
                                self.test_set.should_tree,
                                "Tree compare with SAMPLE_LINE_SHORT not "
                                + "equal to should_tree")


    def test_searching_non_existing_second_delimiter(self):
        """
        Tests the searching of the second delimiter when an non existing
        one is used.
        """
        self._change_second_delimiter(\
            self.test_set.NON_EXISTING_SECOND_DELIMITER)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        self.assert_tree(self.tree_instance,
                                self.test_set.should_tree,
                                "Tree compare with SAMPLE_LINE_SHORT using "
                                + "nonexisting second delimiter not equal "
                                + "to should_tree")


    def test_extracted_identifiers_incl_second_delimiter(self):
        self._change_second_delimiter(\
            self.test_set.EXISTING_SECOND_DELIMITER)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_FULL,
                                self.tree_instance)
        self.assert_tree(self.tree_instance,
            self.test_set.should_tree_including_third_result,
            "Tree compare with SAMPLE_LINE_FULL using "
            + "existing second delimiter not equal to "
            + "should_tree_including_third_result")



    def test_extracted_identifiers_incl_empty_str_2delimiter(self):
        self._change_second_delimiter(\
            self.test_set.EXISTING_SECOND_DELIMITER)
        importer = TextImporter(self._conf)
        importer.interpret_line(
            self.test_set.SAMPLE_LINE_WITH_SECOND_DELIMITER_BUT_WITHOUT_THIRD_RESULT,
            self.tree_instance)
        self.assert_tree(self.tree_instance,
            self.test_set.should_tree_without_3rd_result_but_2nd_delimiter,
            "Tree compare with SAMPLE_LINE_SHORT using existing second " \
            + "delimiter")


    def _change_second_delimiter(self, new_second_delimiter):
        self._conf.data[str(CONFIG_ENUM.SecondDelimiter)] \
 = new_second_delimiter



class ImporterTestCheckInterpreteLineWithData(TreeTestBase):
    """Tests simple tree structure but with data lines
    """


    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_test(self._conf)


    def test_proper_data_prefix_and_line(self):
        """Test data line with proper data prefix and line
        """
        self._change_data_prefix(self.test_set.DATA_PREFIX_STAR)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX,
                                self.tree_instance)
        self.assert_tree(self.tree_instance,
                                self.test_set.should_tree_with_data,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX not "
                                + "equal to should_tree_with_data")


    def test_should_ignore_data_with_dollar_prefix(self):
        self._change_data_prefix(self.test_set.DATA_PREFIX_STAR)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX,
                                     self.tree_instance)
        self.assert_tree(
                                self.tree_instance,
                                self.test_set.should_tree_without_data,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX using"
                                + " nonexisting data prefix not equal to "
                                + "should_tree_without_data")

    def test_data_line_after_non_valid_data_line(self):
        """check whether the data will be correctly processed after an line
        with a non-valid data prefix is processed.
        Test case needed because line with dollar as prefix is moved to the so
        called remainder list and an object attribute
        "ignore_the_following_datalines" is set to True. This indicates the
        next runthrough to ignore data lines because they might have no proper
        tree element to belong to."""        
        self._change_data_prefix(self.test_set.DATA_PREFIX_STAR)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX,
                                     self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        self.assert_tree(
                                self.tree_instance,
                                self.test_set.should_tree_without_data,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX using"
                                + " nonexisting data prefix not equal to "
                                + "should_tree_without_data")

    def test_tree_element_with_data__after_non_valid_data_line(self):
        """check whether the tree element(2) and the data(of 2) will be 
        correctly processed after an line with a non-valid data prefix 
        (of tree element 1) is processed.        
        Test case needed because line with dollar as prefix is moved to the so
        called remainder list and an object attribute
        "ignore_the_following_datalines" is set to True. This indicates the
        next runthrough to ignore data lines because they might have no proper
        tree element to belong to.
        
        """
                
        self._change_data_prefix(self.test_set.DATA_PREFIX_STAR)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_FOR_NON_DATA_TREE,
                                     self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX,
                                     self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX,
                                self.tree_instance)        
        self.assert_tree(
            self.tree_instance,
            self.test_set.should_tree_with_2_branches_but_second_with_data,
            "Tree compare with SAMPLE_LINE_FOR_NON_DATA_TREE and " 
            + "SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX using"
            + " nonexisting data prefix. Afterwards "
            +"SAMPLE_LINE_SHORT will be interpreted. This all is"
            +"not equal to "
            + "should_tree_with_2_branches_but_second_with_data")


    def _change_data_prefix(self, new_data_prefix):
        self._conf.data[str(CONFIG_ENUM.UseDataPrefix)] = True
        self._conf.data[str(CONFIG_ENUM.DataDelimiter)] \
 = new_data_prefix





class ImporterTestCheckInterpreteWithLineAsTreeElements(TreeTestBase):
    """Tests simple tree structure with data lines as own tree elements
    (lowest level)
    """

    def setUp(self):
        self._conf = TestConfigurationSet. \
            retrieve_test_configuration_data_as_treeelements()

        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet. \
            retrieve_shouldtrees_data_as_tree_elements_test(self._conf)


    def test_proper_data_prefix_and_line(self):
        """Test data line with proper data prefix and line
        """
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                self.tree_instance)
        importer.interpret_line(self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX,
                                self.tree_instance)
        self.assert_tree(self.tree_instance,
            self.test_set.should_tree_with_data_tree_elements,
            "Tree compare with SAMPLE_LINE_SHORT and "
            + "SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX not "
            + "equal to should_tree_with_data_tree_elements")


    def test_should_ignore_data_with_dollar_prefix(self):
        importer = TextImporter(self._conf)
        importer.interpret_line(self.test_set.SAMPLE_LINE_SHORT,
                                self.tree_instance)
        importer.interpret_line(
            self.test_set.SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX,
            self.tree_instance)
        self.assert_tree(
                                self.tree_instance,
                                self.test_set.should_tree_without_datatreeelements,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX "
                                + "using nonexisting data prefix not equal to "
                                + "should_tree_without_datatreeelements")



class ImporterTestCheckInterpreteLineIgnoreLine(TreeTestBase):
    """Tests simple tree structure with the option to ignore a line.
    """

    SAMPLE_LINE_SHORT = "@Identifier Foo1"
    SAMPLE_IGNORING_LINE_WITHOUT_PREFIX = "testline"
    SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX = "# " \
        + SAMPLE_IGNORING_LINE_WITHOUT_PREFIX

    IGNORE_PREFIX_HASHMARK = "#"
    IGNORE_PREFIX_DOLLAR = "$"

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)


        self.should_tree = TestConfigurationSet.retrieve_should_tree(self._conf)
        logging.debug("print should_tree")
        tree_operations.print_tree(self.should_tree)

        self.should_tree_with_ignored_line_as_data \
 = copy.deepcopy(self.should_tree)
        last_child = self.should_tree_with_ignored_line_as_data. \
            get_children()[0].get_children()[0]
        last_child.add_line_data(\
            self.SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX)
        logging.debug("print should_tree_with_ignored_line_as_data")
        tree_operations.print_tree(self.should_tree_with_ignored_line_as_data)



    def test_ignore_line_with_proper_ignore_prefix_and_line(self):
        self._change_ignore_prefix(self.IGNORE_PREFIX_HASHMARK)
        importer = TextImporter(self._conf)
        importer.interpret_line(self.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        importer.interpret_line(\
            self.SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX,
            self.tree_instance)
        self.assert_tree(
                                self.tree_instance,
                                self.should_tree,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX "
                                + "ignoring a line beginning with hashmark not "
                                + "equal to should_tree")


    def test_should_ignore_data_with_dollar_prefix(self):
        self._change_ignore_prefix(self.IGNORE_PREFIX_DOLLAR)
        #if the configuration doesn't have an DataPrefix, it will add all
        #non-identifier lines to the data
        self._conf.data[str(CONFIG_ENUM.UseDataPrefix)] = False
        importer = TextImporter(self._conf)
        importer.interpret_line(self.SAMPLE_LINE_SHORT,
                                     self.tree_instance)
        importer.interpret_line(self.SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX,
                                     self.tree_instance)
        self.assert_tree(self.tree_instance,
                                self.should_tree_with_ignored_line_as_data,
                                "Tree compare with SAMPLE_LINE_SHORT and "
                                + "SAMPLE_IGNORING_LINE_WITH_HASHMARK_AS_PREFIX "
                                + "ignoring a line beginning with DOLLAR not "
                                + "equal to should_tree_with_ignored_line_as_data")

    def _change_ignore_prefix(self, new_ignore_prefix):
        self._conf.data[str(CONFIG_ENUM.UseIgnorePrefix)] = True
        self._conf.data[str(CONFIG_ENUM.IgnorePrefix)] \
 = new_ignore_prefix


class ImporterTestCheckRemainderFunction(TreeTestBase):
    """Tests remainder list by just interpreting non-valid line
    """

    SAMPLE_NON_VALID_LINE = "testline"

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)


        self.should_empty_tree = Tree(self._conf)
        logging.debug("print should_empty_tree")
        tree_operations.print_tree(self.should_empty_tree)

        self.should_remainder_list = ["testline"]


    def test_remainder_list_adding_non_valid_line(self):
        importer = TextImporter(self._conf)
        importer.interpret_line(self.SAMPLE_NON_VALID_LINE,
                                     self.tree_instance)
        self.assert_tree(self.tree_instance,
                                self.should_empty_tree,
                                "Tree compare with SAMPLE_NON_VALID_LINE not "
                                 + "equal to should_empty_tree")
        self.assertListEqual(importer.remainder_lines,
                             self.should_remainder_list,
                             "remainderlist doesn't contain the remainded "
                             + "SAMPLE_NON_VALID_LINE")

