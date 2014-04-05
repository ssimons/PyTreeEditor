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


class TreeOperationsDataChangeLabelTest(TreeTestBase):
    """Tests tree operations.
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration_data_as_treeelements()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_as_tree_elements_operations_test(self._conf)

        #stubbing fire_data_change - not needed in here
        when(self.test_set.tree_with_data_tree_elements). \
            fire_data_changed().thenReturn(True)

    def test_delete_data_tree_elements_operation(self):
        """Test the delete operation with the first and third
        tree element (that are data tree elements).

        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, True)

        result_list = tree_operations.remove_element_is_from_tree(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_first_and_last_deleted,
            "Tree compare with tree_with_data_tree_elements after deletion of "
            + "first and last not equal to "
            + "should_tree_first_and_last_deleted")
        self.assertEqual(result_list,
            [],
            "Compare of failed elements of result_list isn't "
            + "equal to empty list []")

    def test_delete_data_of_middle_tree_element(self):
        """Test the delete operation with an tree element which has an parent
        element and also an child (sub) element.
        """

        #tree wasn't regularly build up using the importer -> no order set
        self.test_set.tree_with_data_tree_elements.order_of_elements_references \
 = [self.test_set.tree_with_data_tree_elements.get_children()[0],
               self.test_set.tree_with_data_tree_elements.get_children()[0].get_children()[0]]



        self.test_set.tree_with_data_tree_elements.get_children()[0]. \
            get_children()[0].set_check_state_bool(True)
        result_list = tree_operations.remove_element_is_from_tree(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_after_deleting_middle_element,
            "Tree compare with tree_with_data_tree_elements after deletion of "
            + "middle element not equal to "
            + "should_tree_after_deleting_middle_element")
        self.assertEqual(result_list,
            [],
            "Compare of failed elements of result_list isn't "
            + "equal to empty list []")


        self.assert_str_list_entries(
            self.test_set.tree_with_data_tree_elements.order_of_elements_references,
            self.test_set.should_order_of_elements_of_tree_middle_deleted,
            "Compare of order_of_elements_references elements of "
            + "tree_with_data_tree_elements isn't "
            + "equal to should_order_of_elements_of_tree_middle_deleted")


    def test_delete_an_root_child_element(self):
        """Test the delete operation on an child of root (highgest level).

        """

        tree_with_sub_element = TestConfigurationSet. \
            retrieve_should_tree(self._conf)
        tree_with_sub_element.get_children()[0].set_check_state_bool(True)

        #tree wasn't regularly build up using the importer -> no order set
        tree_with_sub_element.order_of_elements_references \
 = [tree_with_sub_element.get_children()[0],
               tree_with_sub_element.get_children()[0].get_children()[0]]


        result_list = tree_operations.remove_element_is_from_tree(\
            tree_with_sub_element)
        self.assert_tree(
            tree_with_sub_element,
            Tree(self._conf),
            "Tree compare with tree_with_sub_element after deletion of "
            + "highest level element not equal to "
            + "new empty Tree object")
        self.assertEqual(result_list,
            [],
            "Compare of failed elements of result_list isn't "
            + "equal to empty list []")

        self.assertEqual(tree_with_sub_element.order_of_elements_references,
            [],
            "Compare of order_of_elements_references elements of "
            + "tree_with_sub_element.order_of_elements_references isn't "
            + "equal to empty list []")
