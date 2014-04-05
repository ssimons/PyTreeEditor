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
from src.modell.logger import logging
from tests.assistance.tree_test_base import TreeTestBase
from mockito import when

class TreeOperationsDataChangeLabelTest(TreeTestBase):
    """Tests different tree structures using first, second and third delimiter.
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration_data_as_treeelements()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_as_tree_elements_up_down_operations_test(self._conf)

        self.should_result_list_all_up = \
            [self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
             self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX3]
        self.should_result_list_all_down = \
            [self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
             self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX]

        #stubbing fire_data_change - not needed in here
        when(self.test_set.tree_with_data_tree_elements). \
            fire_data_changed().thenReturn(True)

    def test_first_down_operation(self):
        """Test the data down operation with the first of three data
        tree elements
        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, False)

        result_list = tree_operations.data_down_move(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_after_fist_down_op,
            "Tree compare with tree_with_data_tree_elements after down "
            + "operation not equal to "
            + "should_tree_after_fist_down_op")
        self.assertEqual(result_list,
            [self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX],
            "Compare of successfully down moved elements of result_list isn't "
            + "equal to [SAMPLE_DATA_LINE_WITHOUT_PREFIX]")

    def test_last_up_operation(self):
        """Test the data up operation with the last of three data tree elements
        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            False, False, True)

        result_list = tree_operations.data_up_move(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_after_last_up_op,
            "Tree compare with tree_with_data_tree_elements after up "
            + "operation not equal to "
            + "should_tree_after_last_up_op")
        self.assertEqual(result_list,
            [self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX3],
            "Compare of successfully up moved elements of result_list isn't "
            + "equal to [SAMPLE_DATA_LINE_WITHOUT_PREFIX3]")


    def test_all_down_operation(self):
        """Test the data down operation with all three data
        tree elements
        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, True, True)

        result_list = tree_operations.data_down_move(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_after_all_down_op,
            "Tree compare with tree_with_data_tree_elements after down "
            + "operation not equal to "
            + "should_tree_after_all_down_op")
        logging.debug("Compare of successfully down moved elements of "
            + "result_list isn't "
            + "equal to should_result_list_all_down: " + "".join(result_list)
            + " vs. " + "".join(self.should_result_list_all_down))
        self.assertEqual(result_list, self.should_result_list_all_down,
            "Compare of successfully down moved elements of result_list isn't "
            + "equal to should_result_list_all_down")

    def test_all_up_operation(self):
        """Test the data up operation with all three data
        tree elements
        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, True, True)

        result_list = tree_operations.data_up_move(
            self.test_set.tree_with_data_tree_elements)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_after_all_up_op,
            "Tree compare with tree_with_data_tree_elements after up "
            + "operation not equal to "
            + "should_tree_after_all_up_op")
        logging.debug("Compare of successfully up moved elements of "
            + "result_list isn't equal to "
            + "should_result_list_all_up: " + "".join(result_list) + " vs. "
            + "".join(self.should_result_list_all_up))
        self.assertEqual(result_list, self.should_result_list_all_up,
            "Compare of successfully up moved elements of result_list isn't "
            + "equal to should_result_list_all_up")

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
