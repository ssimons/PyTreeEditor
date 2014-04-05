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
from src.modell.importer import TextImporter


class TreeOperationsCopyWithDataTest(TreeTestBase):
    """Tests the copy functionality from one to another tree with data
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_test(self._conf)
        self.test_set_clone \
 = TestConfigurationSet.retrieve_shouldtrees_data_test(self._conf)

        #stubbing fire_data_change - not needed in here
        when(self.test_set.should_tree_with_data). \
            fire_data_changed().thenReturn(True)
        when(self.test_set_clone.should_tree_with_data). \
            fire_data_changed().thenReturn(True)

    def test_copy_with_data(self):
        """Test the copy functionality from one to another tree with data.
        """

        #set element as checked
        last_child \
 = self.test_set.should_tree_with_data.get_children()[0].get_children()[0]
        last_child.set_check_state_bool(True)

        result_list = tree_operations.copy_elements_to_other_tree(
            self.test_set.should_tree_with_data,
            self.tree_instance,
            self._conf)

        self.assert_tree(self.tree_instance,
                        self.test_set.should_tree_with_data,
                       "Tree compare with tree_instance after copy from "
                       + "should_tree_with_data "
                       + "operation not equal to should_tree_with_data")
        self.assertEqual(
           result_list, [],
           "Compare of remainder list (ignored lines) which weren't copied "
           + "from one tree to another tree aren't equal to []")



    def test_copy_already_existing_tree_element(self):
        """Test the copy functionality from one to another tree with two equal
        trees. Therefore the incoming tree element shouldn't be imported.
        """

        #set element as checked
        last_child \
 = self.test_set.should_tree_with_data.get_children()[0].get_children()[0]
        last_child.set_check_state_bool(True)


        result_list = tree_operations.copy_elements_to_other_tree(
             self.test_set.should_tree_with_data,
             self.test_set_clone.should_tree_with_data,
             self._conf)

        self.assert_tree(self.test_set_clone.should_tree_with_data,
                         self.test_set.should_tree_with_data,
                        "Tree compare with should_tree_with_data after "
                        + "copy from the equal should_tree_with_data "
                        + "operation not equal to should_tree_with_data")
        self.assertEqual(result_list,
            [TextImporter.DUPLICATE_STR + self.test_set.SAMPLE_LINE_SHORT,
            self.test_set.SAMPLE_DATA_LINE_WITH_STAR_AS_PREFIX],
            "Compare of remainder list (ignored lines) which weren't copied "
            + "from one tree to another tree aren't equal to []")



class TreeOperationsCopyWithDataElementsTest(TreeTestBase):
    """Tests the copy functionality from one to another tree with data tree
    elements.
    """

    def setUp(self):
        self._conf = TestConfigurationSet.retrieve_test_configuration_data_as_treeelements()
        self.tree_instance = Tree(self._conf)

        self.test_set \
 = TestConfigurationSet.retrieve_shouldtrees_data_as_tree_elements_up_down_operations_test(self._conf)

        #stubbing fire_data_change - not needed in here
        when(self.test_set.tree_with_data_tree_elements). \
            fire_data_changed().thenReturn(True)

    def test_copy_with_data_tree_elements(self):
        """Test the copy functionality from one to another tree with data tree
    elements.
        """
        self._set_check_state_of_3dataelements(
            self.test_set.tree_with_data_tree_elements,
            True, False, False)
        result_list = tree_operations.copy_elements_to_other_tree(
             self.test_set.tree_with_data_tree_elements,
             self.tree_instance,
             self._conf)
        self.assert_tree(
            self.tree_instance,
            self.test_set.tree_with_data_tree_elements,
            "Tree compare with tree_instance after copy from "
            + "tree_with_data_tree_elements "
            + "operation not equal to tree_with_data_tree_elements")
        self.assertEqual(
            result_list, [],
            "Compare of remainder list (ignored lines) which weren't copied "
            + "from one tree to another tree aren't equal to []")
