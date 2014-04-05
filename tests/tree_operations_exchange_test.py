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

from tests.assistance.test_set import TestConfigurationSet
from src.modell.treestruct.tree_element import Tree
from src.modell import tree_operations
from tests.assistance.tree_test_base import TreeTestBase
from mockito import when
from src.modell.treestruct.tree_exceptions import \
    NotEnoughTreeElementsCheckedException, NoProperTreeElementException,\
    TreeElementsNotSameLevelException
from src.modell.logger import logging

class TreeOperationsDataChangeLabelTest(TreeTestBase):
    """Tests tree element exchange functionality.
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration_data_as_treeelements()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_as_tree_elements_exchange_operations_test(self._conf)

        #stubbing fire_data_change - not needed in here
        when(self.test_set.tree_with_data_tree_elements). \
            fire_data_changed().thenReturn(True)

    def test_exchange_not_enough_checked_elements(self):
        """Test the exchange operation but with not enough checked elements.
        Therefore an excpetion is expected-

        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, False)
        with self.assertRaises(NotEnoughTreeElementsCheckedException):
            tree_operations.exchange_elements(
                self.test_set.tree_with_data_tree_elements)

    def test_exchange_not_allowed_mix_of_tree_types(self):
        """Test the exchange operation but with an data tree element and an
        typical tree elemtn.
        Therefore an excpetion is expected-

        """
        #set the first data tree element as checked
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, False)
        #also set the first child as checked:
        self.test_set.tree_with_data_tree_elements.get_children()[0]. \
            set_check_state_bool(True)

        with self.assertRaises(NoProperTreeElementException):
            tree_operations.exchange_elements(
                self.test_set.tree_with_data_tree_elements)




    def test_exchange_data_tree_elements_same_parent(self):
        """Test the exchange operation with data tree elements of the same
        parent element.
        Additionally the order_of_elements_references is compared to the value
        before the test. It should be equal (not altered for data tree elements).
        """
        order_before_test \
 = self.test_set.tree_1_branch_with_data_tree_elements_and_one_without. \
                order_of_elements_references

        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, True)
        tree_operations.exchange_elements(
                self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_exchanged_first_and_last_of_same_parent,
            "Tree compare with tree_with_data_tree_elements after exchange "
            + "operation not equal to "
            + "should_tree_exchanged_first_and_last_of_same_parent")
        self.assertEquals(self.test_set.tree_1_branch_with_data_tree_elements_and_one_without. \
            order_of_elements_references, order_before_test,
            "Order to print ot file isn't equal to should one")

    def test_exchange_data_tree_elements_different_parent(self):
        """Test the exchange operation with data tree elements of different
        parent elements (means every data tree element has its own parent
        element).
        Additionally the order_of_elements_references is compared to the value
        before the test. It should be equal (not altered for data tree elements).

        """
        order_before_test \
 = self.test_set.tree_1_branch_with_data_tree_elements_and_one_without. \
                order_of_elements_references

        tree_operations.exchange_elements(
                self.test_set.tree_with_2_branches_each_with_data_tree_element)
        self.assert_tree(
            self.test_set.tree_with_2_branches_each_with_data_tree_element,
            self.test_set.should_2branches_each_data_tree_element_exchanged,
            "Tree compare with tree_with_2_branches_each_with_data_tree_element"
            + " after exchange "
            + "operation not equal to "
            + "should_2branches_each_data_tree_element_exchanged")
        self.assertEquals(self.test_set.tree_1_branch_with_data_tree_elements_and_one_without. \
            order_of_elements_references, order_before_test,
            "Order to print ot file isn't equal to should one")

    def test_exchange_tree_elements_different_parent(self):
        """Test the exchange operation with normal tree elements of different
        parent elements (means every data tree element has its own parent
        element).
        Additionally the order_of_elements_references is compared to the value
        before the test. It should be equal (not altered for data tree elements).

        """
        #tree wasn't regularly build up using the importer -> no order set
        self.test_set.tree_1_branch_with_data_tree_elements_and_one_without. \
            order_of_elements_references = self.test_set.tree_1_branch_order_of_elements

        list_of_str_tree_elements = []
        for current_element in self.test_set.tree_1_branch_order_of_elements:
            list_of_str_tree_elements.append(current_element.label_name)
        logging.debug("order_of_elements before test: %s",
                      "".join(list_of_str_tree_elements))


        with self.assertRaises(TreeElementsNotSameLevelException):
            tree_operations.exchange_elements(
                self.test_set.tree_1_branch_with_data_tree_elements_and_one_without)

        self.assert_tree(
            self.test_set.tree_1_branch_with_data_tree_elements_and_one_without,
            self.test_set.should_tree_1_branch_with_data_tree_elements_and_one_without,
            "Tree compare with "
            + "tree_1_branch_with_data_tree_elements_and_one_without"
            + " after exchange "
            + "operation not equal to "
            + "should_tree_1_branch_with_data_tree_elements_and_one_without")

        #compare the order of the incoming elements
        self.assert_str_list_entries(
            self.test_set.tree_1_branch_with_data_tree_elements_and_one_without.\
                order_of_elements_references,
            self.test_set.should_tree_1_branch_order_of_elements,
            "Order to print ot file isn't equal to should one")
