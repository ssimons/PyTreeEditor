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

        self.should_result_list_replaced = \
            [self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
             self.test_set.SAMPLE_DATA_LINE_WITHOUT_PREFIX3]

        #stubbing fire_data_change - not needed in here
        when(self.test_set.tree_with_data_tree_elements). \
            fire_data_changed().thenReturn(True)

    def test_replace_operation(self):
        """Test the replace/ change label operation with the first and third
        tree element (that are data tree elements).

        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, True)

        result_list = tree_operations.tree_element_change_label(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.SAMPLE_DATA_LINE_FOR_REPLACE_TEST)
        self.assert_tree(
            self.test_set.tree_with_data_tree_elements,
            self.test_set.should_tree_first_and_last_replaced,
            "Tree compare with tree_with_data_tree_elements after replace "
            + "operation not equal to "
            + "should_tree_first_and_last_replaced")
        self.assertEqual(result_list,
            self.should_result_list_replaced,
            "Compare of successfully replaced elements of result_list isn't "
            + "equal to should_result_list_replaced")
