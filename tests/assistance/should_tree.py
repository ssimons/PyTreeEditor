#!/usr/bin/python
# -*- coding: utf-8*-

"""

Tree Editor.
Copyright (C) 2014  ssimons

    Contains the should trees of the test_set.

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


from src.modell.enumerations import TREE_LEVEL_ENUM
from src.modell.treestruct.tree_element import TreeElement, Tree
from src.modell import tree_operations
from src.modell.logger import logging
import copy
import tests.assistance.test_set


class ShouldTreesDelimiter(object):
    SAMPLE_LINE_SHORT = "@Identifier Foo1"
    SAMPLE_LINE_FULL = "@Identifier Foo1 | LastPart"
    SAMPLE_LINE_WITH_SECOND_DELIMITER_BUT_WITHOUT_THIRD_RESULT \
 = "@Identifier Foo1 | "
    EXISTING_SECOND_DELIMITER = " | "
    NON_EXISTING_SECOND_DELIMITER = "$"



    def __init__(self, configuration):
        self.should_tree = \
            tests.assistance.test_set.TestConfigurationSet. \
            retrieve_should_tree(configuration)
        logging.debug("print should_tree")
        tree_operations.print_tree(self.should_tree)

        self.should_tree_including_third_result \
 = copy.deepcopy(self.should_tree)
        parent_of_new_child = self.should_tree_including_third_result. \
            get_children()[0].get_children()[0]
        should_tree_including_third_result_child = TreeElement("LastPart",
                                TREE_LEVEL_ENUM.CHILD_OF_CHILD,
                                parent_of_new_child)
        parent_of_new_child.add_children_without_modelnotify(\
            should_tree_including_third_result_child)
        logging.debug("print should_tree_including_third_result")
        tree_operations.print_tree(self.should_tree_including_third_result)

        #should tree without third result but appended second delimiter
        self.should_tree_without_3rd_result_but_2nd_delimiter \
 = copy.deepcopy(self.should_tree)
        first_child = self.should_tree_without_3rd_result_but_2nd_delimiter. \
            get_children()[0].get_children()[0]
        first_child.change_label("Foo1 | ")
        logging.debug("print " \
            + "should_tree_without_3rd_result_but_2nd_delimiter")
        tree_operations.print_tree(self. \
            should_tree_without_3rd_result_but_2nd_delimiter)

class ShouldTreesForDataTests(object):

    SAMPLE_LINE_SHORT = "@Identifier Foo1"
    SAMPLE_LINE_FOR_NON_DATA_TREE = "@Identifier FooNON"
    SAMPLE_DATA_LINE_WITHOUT_PREFIX = "PKT TT 1865 0 10"
    SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX = "*" \
        + SAMPLE_DATA_LINE_WITHOUT_PREFIX
    SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX = "$" \
        + SAMPLE_DATA_LINE_WITHOUT_PREFIX

    DATA_PREFIX_STAR = "*"

    def __init__(self, configuration):

        self.should_tree_without_data \
 = tests.assistance.test_set.TestConfigurationSet.retrieve_should_tree(configuration)
        logging.debug("print should_tree_without_data")
        tree_operations.print_tree(self.should_tree_without_data)

        self.should_tree_with_data \
 = copy.deepcopy(self.should_tree_without_data)
        last_child \
 = self.should_tree_with_data.get_children()[0].get_children()[0]
        last_child.add_line_data(self.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX)
        logging.debug("print should_tree_with_data")
        tree_operations.print_tree(self.should_tree_with_data)

        #2 branches  - the second one contains data element
        self.should_tree_with_2_branches_but_second_with_data \
            = Tree(configuration)
        should_root_of_2branches = TreeElement("Identifier",
                                TREE_LEVEL_ENUM.ROOT,
                                self.should_tree_with_2_branches_but_second_with_data)
        self.should_tree_with_2_branches_but_second_with_data. \
            add_children_without_modelnotify(should_root_of_2branches)
        should_branch1 = TreeElement("FooNON",
                                TREE_LEVEL_ENUM.CHILD,
                                should_root_of_2branches)
        should_root_of_2branches.add_children_without_modelnotify( \
            should_branch1)
        should_branch2 = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_root_of_2branches)
        should_root_of_2branches.add_children_without_modelnotify(\
            should_branch2)
        
        #add data to branch 2
        should_branch2.add_line_data(self.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX)
        logging.debug("print should_tree_with_2_branches_but_second_with_data")
        tree_operations.print_tree( \
            self.should_tree_with_2_branches_but_second_with_data)
                

class ShouldTreesWithDataAsTreeElements(object):

    SAMPLE_LINE_SHORT = "@Identifier Foo1"
    SAMPLE_DATA_LINE_WITHOUT_PREFIX = "PKT TT 1865 0 10"
    SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX = "*" \
        + SAMPLE_DATA_LINE_WITHOUT_PREFIX
    SAMPLE_DATA_LINE_WITH_DOLLAR_AS_PREFIX = "$" \
        + SAMPLE_DATA_LINE_WITHOUT_PREFIX


    def __init__(self, configuration):

        self.should_tree_without_datatreeelements \
 = tests.assistance.test_set.TestConfigurationSet.retrieve_should_tree(configuration)
        logging.debug("print should_tree_without_datatreeelements")
        tree_operations.print_tree(self.should_tree_without_datatreeelements)

        self.should_tree_with_data_tree_elements \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_with_data_tree_elements. \
            get_children()[0].get_children()[0]
        should_tree_data_child = TreeElement(self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
                                             TREE_LEVEL_ENUM.DATA_EXPANDED,
                                             last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child)
        logging.debug("print should_tree_with_data_tree_elements")
        tree_operations.print_tree(self.should_tree_with_data_tree_elements)




