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

from src.modell import tree_operations
from src.modell.logger import logging
from src.modell.treestruct.tree_element import TreeElement, Tree
from tests.assistance.test_set import TestConfigurationSet


class TreeTestBase(unittest.TestCase):
    '''
    Base class to test trees using the self-defined function assert_tree.
    setUp function is not needed in derived class because it is defined in here.
    '''
    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_delimiter_test(self._conf)


    def assert_tree(self,
                    tree_instance,
                    should_tree_instance,
                    message):
        """assert function implementaion to compare two trees (given and
        should-be value). Compares recursively all childs / levels of the two
        given tree objects.
        Uses different assert functions of the given test class
        (e.g. assertEquals)
        """
        logging.debug("TreeTestBase.assert_tree: tree_instance")
        tree_operations.print_tree(tree_instance)

        logging.debug("assert_tree: tree_instance.label_name =%s "
                      + "should_tree_instance.label_name=%s",
                      tree_instance.label_name,
                      should_tree_instance.label_name)

        self.assertEquals(tree_instance.label_name,
                                         should_tree_instance.label_name,
                                         message + " Not same name/label: <"
                                         + tree_instance.label_name + "> vs. <"
                                         + should_tree_instance.label_name + ">")

        if isinstance(tree_instance, TreeElement):
            self.assertEquals(tree_instance.tree_level,
                                             should_tree_instance.tree_level,
                                             message + " Not same tree_level: "
                                             + str(tree_instance.tree_level)
                                             + " vs. "
                                             + str(should_tree_instance.tree_level))

            self.assertEquals(tree_instance.line_data,
                                         should_tree_instance.line_data,
                                         message + " Not same line_data: "
                                         + str(tree_instance.line_data)
                                         + " vs. "
                                         + str(should_tree_instance.line_data))


        children_elements = tree_instance.get_children()
        should_children_elements = should_tree_instance.get_children()


        len_children_elements = len(children_elements)
        len_should_children_elements = len(should_children_elements)
        logging.debug("assert_tree: tree_instance children count:%s " \
                      + "should_tree_instance children count:%s",
                      len_children_elements,
                      len_should_children_elements)
        self.assertEquals(len_children_elements,
                                         len_should_children_elements,
                                         message + " Not the same children count:"
                                         + str(len_children_elements) + " vs "
                                         + str(len_should_children_elements))

        for i in range(len(children_elements)):
            self.assert_tree(
                children_elements[i],
                should_children_elements[i],
                message)


    def _set_check_state_of_3dataelements(self, tree_instance,
        first_selected_bool, second_selected_bool, third_selected_bool):
        """ internal function to preselect the information whether the 3 data
        elements should be selected or not """

        parent_of_data_elements = tree_instance.get_children()[0]. \
            get_children()[0]
        parent_of_data_elements.get_children()[0]. \
            set_check_state_bool(first_selected_bool)
        parent_of_data_elements.get_children()[1]. \
            set_check_state_bool(second_selected_bool)
        parent_of_data_elements.get_children()[2]. \
            set_check_state_bool(third_selected_bool)

    def assert_str_list_entries(self, list_of_tree_elements,
            should_list_of_tree_elements, message):
        """Compares every entry of the list as str objects.
        Other values of the objects might influence the comparison.
        order_of_elements_references is good candidate for this function.
        """
        list_of_str = []
        for current_element in list_of_tree_elements:
            list_of_str.append(current_element.label_name)
        logging.debug("assert_str_list_entries: list as str entries:  %s",
                      "".join(list_of_str))

        list_of_should_str = []
        for should_element in should_list_of_tree_elements:
            list_of_should_str.append(should_element.label_name)
        logging.debug("assert_str_list_entries:  "
            + "should_list_of_tree_elements as str entries: "
            + "".join(list_of_should_str))

        self.assertEquals(list_of_str,
                         list_of_should_str,
                         message + " Not same list entries: <"
                         + "".join(list_of_str) + "> vs. <"
                         + "".join(list_of_should_str) + ">")

