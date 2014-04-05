#!/usr/bin/python
# -*- coding: utf-8*-
"""

Tree Editor.
Copyright (C) 2014  ssimons

    Module Contains the should trees of the test_set for the tree operations tests.

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
from src.modell.treestruct.tree_element import Tree, TreeElement
from src.modell import tree_operations
from src.modell.logger import logging
import copy
import tests.assistance.test_set


class BaseShouldTreesWithDataAsTreeElementsOperations(object):
    """ Test set for trees with data as tree elements.
    Typically this class is derived.
    """

    SAMPLE_DATA_LINE_WITHOUT_PREFIX = "PKT TT 1865 0 10"
    SAMPLE_DATA_LINE_WITHOUT_PREFIX2 = "ELEM 11 65 16 0"
    SAMPLE_DATA_LINE_WITHOUT_PREFIX3 = "NUM AA 10 56 100"
    SAMPLE_DATA_LINE_FOR_REPLACE_TEST = "PKT 1234567890"

    def __init__(self, configuration):

        self.should_tree_without_datatreeelements \
 = tests.assistance.test_set.TestConfigurationSet. \
            retrieve_should_tree(configuration)


        #tree with data as selements: 1,2,3 in order
        self.tree_with_data_tree_elements \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.tree_with_data_tree_elements. \
            get_children()[0].get_children()[0]

        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)

        last_child.add_children_without_modelnotify(should_tree_data_child1)
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)

        logging.debug("print tree_with_data_tree_elements")
        tree_operations.print_tree(self.tree_with_data_tree_elements)




class ShouldTreesWithDataAsTreeElementsUpDownOperations(
        BaseShouldTreesWithDataAsTreeElementsOperations):
    """ From BaseShouldTreesWithDataAsTreeElementsOperations derived
    test set for trees with data as tree elements but for special
    operations like up and down move of the selected elements.
    Furthermore the same tree after the up and one for after the down operation
    (as should variants) are provided.
    All reference trees (should_*) are build analog to
    tree_with_data_tree_elements,
    which is the one that will be used in the test case).
    """

    def __init__(self, configuration):
        super(ShouldTreesWithDataAsTreeElementsUpDownOperations, self). \
            __init__(configuration)

        #should tree after the up operation of the last element: 1,3,2 in order
        self.should_tree_after_last_up_op \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_after_last_up_op. \
            get_children()[0].get_children()[0]
        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child1)
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        logging.debug("print should_tree_after_last_up_op")
        tree_operations.print_tree(self.should_tree_after_last_up_op)


        #should tree after the down operation of the first element: 2,1,3 in order
        self.should_tree_after_fist_down_op \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_after_fist_down_op. \
            get_children()[0].get_children()[0]
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child1)
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)

        logging.debug("print should_tree_after_fist_down_op")
        tree_operations.print_tree(self.should_tree_after_fist_down_op)


        #should tree after the up operation: 2,3,1 in order
        self.should_tree_after_all_up_op \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_after_all_up_op. \
            get_children()[0].get_children()[0]

        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)
        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child1)


        logging.debug("print should_tree_after_all_up_op")
        tree_operations.print_tree(self.should_tree_after_all_up_op)


        #should tree after the down operation: 3,1,2 in order
        self.should_tree_after_all_down_op \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_after_all_down_op. \
            get_children()[0].get_children()[0]
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)
        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child1)
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        logging.debug("print should_tree_after_all_down_op")
        tree_operations.print_tree(self.should_tree_after_all_down_op)

class ShouldTreesWithDataAsTreeElementsOperations(
        BaseShouldTreesWithDataAsTreeElementsOperations):
    """ From BaseShouldTreesWithDataAsTreeElementsOperations derived
    test set for trees with data as tree elements but for special
    operations like replace selected elements.
    Furthermore the same tree after the operations
    (as should variants) are provided.
    All reference trees (should_*) are build analog to
    tree_with_data_tree_elements,
    which is the one that will be used in the test case).
    """

    def __init__(self, configuration):
        super(ShouldTreesWithDataAsTreeElementsOperations, self).\
            __init__(configuration)

        #should tree after replace operation: 1 and 3 should be replaced
        self.should_tree_first_and_last_replaced \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_first_and_last_replaced. \
            get_children()[0].get_children()[0]

        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_FOR_REPLACE_TEST,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)

        last_child.add_children_without_modelnotify(should_tree_data_child1)
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_FOR_REPLACE_TEST,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)

        logging.debug("print should_tree_first_and_last_replaced")
        tree_operations.print_tree(self.should_tree_first_and_last_replaced)


        #should tree after deletion of first and last data tree element
        self.should_tree_first_and_last_deleted \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_first_and_last_deleted. \
            get_children()[0].get_children()[0]
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        logging.debug("print should_tree_first_and_last_deleted")
        tree_operations.print_tree(self.should_tree_first_and_last_deleted)


        #should tree after deletion of middle element (in this case no sub element are existing)
        self.should_tree_after_deleting_middle_element = Tree(configuration)
        should_first_child_elem = TreeElement("Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.should_tree_after_deleting_middle_element)
        self.should_tree_after_deleting_middle_element.\
            add_children_without_modelnotify(should_first_child_elem)
        logging.debug("print should_tree_after_deleting_middle_element")
        tree_operations.print_tree(self. \
            should_tree_after_deleting_middle_element)

        self.should_order_of_elements_of_tree_middle_deleted = \
            [self.should_tree_after_deleting_middle_element.get_children()[0]]


class ShouldTreesWithDataAsTreeElementsExchangeOperations(
        BaseShouldTreesWithDataAsTreeElementsOperations):
    """ From BaseShouldTreesWithDataAsTreeElementsOperations derived
    test set for trees with data as tree elements but for special
    operations like replace selected elements.
    Furthermore the same tree after the operations
    (as should variants) are provided.
    All reference trees (should_*) are build analog to
    tree_with_data_tree_elements,
    which is the one that will be used in the test case).
    """

    def __init__(self, configuration):
        super(ShouldTreesWithDataAsTreeElementsExchangeOperations, self). \
            __init__(configuration)

        #should tree with first and last element exchanged
        self.should_tree_exchanged_first_and_last_of_same_parent \
 = copy.deepcopy(self.should_tree_without_datatreeelements)
        last_child = self.should_tree_exchanged_first_and_last_of_same_parent. \
            get_children()[0].get_children()[0]
        should_tree_data_child3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX3,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child3)
        should_tree_data_child2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child2)
        should_tree_data_child1 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            last_child)
        last_child.add_children_without_modelnotify(should_tree_data_child1)

        logging.debug("print"
            + "should_tree_exchanged_first_and_last_of_same_parent")
        tree_operations.print_tree(
            self.should_tree_exchanged_first_and_last_of_same_parent)


        #tree with two branches (every branch has its own data tree element)
        #already checked
        self.tree_with_2_branches_each_with_data_tree_element \
 = Tree(configuration)
        should_first_child_elem2 = TreeElement("Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.tree_with_2_branches_each_with_data_tree_element)
        self.tree_with_2_branches_each_with_data_tree_element. \
            add_children_without_modelnotify(should_first_child_elem2)
        should_first_child_of_child_elem2 = TreeElement("Foo1",
            TREE_LEVEL_ENUM.CHILD,
            should_first_child_elem2)
        should_first_child_elem2.add_children_without_modelnotify(\
            should_first_child_of_child_elem2)
        should_second_child_of_child_elem = TreeElement("Foo1",
            TREE_LEVEL_ENUM.CHILD,
            should_first_child_elem2)
        should_first_child_elem2.add_children_without_modelnotify(\
            should_second_child_of_child_elem)
        first_child = self.tree_with_2_branches_each_with_data_tree_element. \
            get_children()[0].get_children()[0]
        second_child = self.tree_with_2_branches_each_with_data_tree_element. \
            get_children()[0].get_children()[1]
        first_child_data_element2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            first_child)
        first_child_data_element2.set_check_state_bool(True)
        first_child.add_children_without_modelnotify(first_child_data_element2)
        second_child_data_element2 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            second_child)
        second_child_data_element2.set_check_state_bool(True)
        second_child.add_children_without_modelnotify(
            second_child_data_element2)
        logging.debug("print tree_with_2_branches_each_with_data_tree_element")
        tree_operations.print_tree(
            self.tree_with_2_branches_each_with_data_tree_element)


        #should variant: tree with two branches (every branch has its own data
        #tree element) where the two data tree elements (with different
        #parents) are exchanged
        self.should_2branches_each_data_tree_element_exchanged \
 = Tree(configuration)
        should_first_child_elem3 = TreeElement("Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.should_2branches_each_data_tree_element_exchanged)
        self.should_2branches_each_data_tree_element_exchanged. \
            add_children_without_modelnotify(should_first_child_elem3)
        should_first_child_of_child_elem = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_first_child_elem3)
        should_first_child_elem3.add_children_without_modelnotify(\
            should_first_child_of_child_elem)
        should_second_child_of_child_elem3 = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_first_child_elem3)
        should_first_child_elem3.add_children_without_modelnotify(\
            should_second_child_of_child_elem3)
        first_child = self.should_2branches_each_data_tree_element_exchanged. \
            get_children()[0].get_children()[0]
        second_child = self.should_2branches_each_data_tree_element_exchanged. \
            get_children()[0].get_children()[1]
        second_child_data_element3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            first_child)
        first_child.add_children_without_modelnotify(second_child_data_element3)
        first_child_data_element3 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            second_child)
        second_child.add_children_without_modelnotify(first_child_data_element3)
        logging.debug("print should_2branches_each_data_tree_element_exchanged")
        tree_operations.print_tree(
            self.should_2branches_each_data_tree_element_exchanged)




        #tree with two branches (one of them has two data tree element childs)
        #already checked
        self.tree_1_branch_with_data_tree_elements_and_one_without \
 = Tree(configuration)
        should_first_child_elem4 = TreeElement("Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.tree_1_branch_with_data_tree_elements_and_one_without)
        self.tree_1_branch_with_data_tree_elements_and_one_without. \
            add_children_without_modelnotify(should_first_child_elem4)
        should_second_child_elem4 = TreeElement("Second-Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.tree_1_branch_with_data_tree_elements_and_one_without)
        should_second_child_elem4.set_check_state_bool(True)
        self.tree_1_branch_with_data_tree_elements_and_one_without. \
            add_children_without_modelnotify(should_second_child_elem4)

        should_first_child_of_child_elem4 = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_first_child_elem4)
        should_first_child_elem4.add_children_without_modelnotify(\
            should_first_child_of_child_elem4)
        should_first_sub_child4 = TreeElement("Foo1-1",
                                TREE_LEVEL_ENUM.CHILD_OF_CHILD,
                                should_first_child_of_child_elem4)
        should_first_sub_child4.set_check_state_bool(True)
        should_first_child_of_child_elem4.add_children_without_modelnotify(\
            should_first_sub_child4)
        should_tree_data_child4 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            should_first_sub_child4)
        should_first_sub_child4.add_children_without_modelnotify(
            should_tree_data_child4)
        should_tree_data_child4b = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            should_first_sub_child4)
        should_first_sub_child4.add_children_without_modelnotify(
            should_tree_data_child4b)

        logging.debug("print tree_1_branch_with_"
                      + "data_tree_elements_and_one_without")
        tree_operations.print_tree(
            self.tree_1_branch_with_data_tree_elements_and_one_without)


        self.tree_1_branch_order_of_elements = \
            [should_first_child_elem4, should_second_child_elem4, \
             should_first_child_of_child_elem4, should_first_sub_child4]


        #should tree with two branches (one of them has
        #two data tree element childs)
        self.should_tree_1_branch_with_data_tree_elements_and_one_without \
 = Tree(configuration)
        should_first_child_elem5 = TreeElement("Identifier",
            TREE_LEVEL_ENUM.ROOT,
            self.should_tree_1_branch_with_data_tree_elements_and_one_without)
        self.should_tree_1_branch_with_data_tree_elements_and_one_without. \
            add_children_without_modelnotify(should_first_child_elem5)

        should_second_child_elem5 = TreeElement("Foo1-1",
            TREE_LEVEL_ENUM.ROOT,
            self.should_tree_1_branch_with_data_tree_elements_and_one_without)
        should_second_child_elem5.set_check_state_bool(True)
        self.should_tree_1_branch_with_data_tree_elements_and_one_without. \
            add_children_without_modelnotify(should_second_child_elem5)

        should_first_child_of_child_elem5 = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_first_child_elem5)
        should_first_child_elem5.add_children_without_modelnotify(\
            should_first_child_of_child_elem5)
        should_first_sub_child5 = TreeElement("Second-Identifier",
                                TREE_LEVEL_ENUM.CHILD_OF_CHILD,
                                should_first_child_of_child_elem5)
        should_first_sub_child5.set_check_state_bool(True)
        should_first_child_of_child_elem5.add_children_without_modelnotify(\
            should_first_sub_child5)

        should_tree_data_child5 = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            should_second_child_elem5)
        should_second_child_elem5.add_children_without_modelnotify(
            should_tree_data_child5)
        should_tree_data_child5b = TreeElement(
            self.SAMPLE_DATA_LINE_WITHOUT_PREFIX2,
            TREE_LEVEL_ENUM.DATA_EXPANDED,
            should_second_child_elem5)
        should_second_child_elem5.add_children_without_modelnotify(
            should_tree_data_child5b)

        logging.debug("print "
            + "should_tree_1_branch_with_data_tree_elements_and_one_without")
        tree_operations.print_tree(
            self.should_tree_1_branch_with_data_tree_elements_and_one_without)


        self.should_tree_1_branch_order_of_elements = \
            [should_first_child_elem5, should_second_child_elem5, \
             should_first_child_of_child_elem5, should_first_sub_child5]
