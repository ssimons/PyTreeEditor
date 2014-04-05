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

from src.modell.enumerations import CONFIG_ENUM, TREE_LEVEL_ENUM
from src.config.configuration import Configuration
from src.modell.treestruct.tree_element import Tree, TreeElement
from tests.assistance.should_tree_operations import ShouldTreesWithDataAsTreeElementsUpDownOperations, \
    ShouldTreesWithDataAsTreeElementsOperations, \
    ShouldTreesWithDataAsTreeElementsExchangeOperations
from tests.assistance.should_tree import ShouldTreesForDataTests, \
    ShouldTreesWithDataAsTreeElements, ShouldTreesDelimiter

class TestConfigurationSet(object):
    """ Typical test tests which are used in many unit tests.

    """
    DATA_DELIMITER = "*"
    DATA_PREFIX_STAR = "*"

    @staticmethod
    def retrieve_test_configuration():
        """Retrieves a typical test configuration preset
        """
        conf = Configuration()

        conf.data[str(CONFIG_ENUM.PreSequence)] = "@"
        conf.data[str(CONFIG_ENUM.FirstDelimiter)] = " "
        conf.data[str(CONFIG_ENUM.SecondDelimiter)] = ""
        conf.data[str(CONFIG_ENUM.UseDataPrefix)] = True
        conf.data[str(CONFIG_ENUM.DataDelimiter)] \
 = TestConfigurationSet.DATA_DELIMITER

        return conf

    @staticmethod
    def retrieve_test_configuration_data_as_treeelements():
        """Retrieves a typical test configuration preset
        """
        conf = TestConfigurationSet.retrieve_test_configuration()
        conf.data[str(CONFIG_ENUM.UseDataPrefix)] = True
        conf.data[str(CONFIG_ENUM.UseDataExpandableInTree)] = True
        conf.data[str(CONFIG_ENUM.DataDelimiter)] \
 = TestConfigurationSet.DATA_DELIMITER
        return conf


    @staticmethod
    def retrieve_should_tree(configuration):
        """retrieves a standard tree without data:
        -Identifier
          +Foo1
          
        """
        should_tree = Tree(configuration)
        should_first_child_elem = TreeElement("Identifier",
                                TREE_LEVEL_ENUM.ROOT,
                                should_tree)
        should_tree.add_children_without_modelnotify(should_first_child_elem)
        should_first_child_of_child_elem = TreeElement("Foo1",
                                TREE_LEVEL_ENUM.CHILD,
                                should_first_child_elem)
        should_first_child_elem.add_children_without_modelnotify(\
            should_first_child_of_child_elem)
        return should_tree

    @staticmethod
    def retrieve_shouldtrees_delimiter_test(configuration):
        return ShouldTreesDelimiter(configuration)

    @staticmethod
    def retrieve_shouldtrees_data_test(configuration):
        return ShouldTreesForDataTests(configuration)

    @staticmethod
    def retrieve_shouldtrees_data_as_tree_elements_test(configuration):
        return ShouldTreesWithDataAsTreeElements(configuration)

    @staticmethod
    def retrieve_shouldtrees_data_as_tree_elements_up_down_operations_test(configuration):
        return ShouldTreesWithDataAsTreeElementsUpDownOperations(configuration)

    @staticmethod
    def retrieve_shouldtrees_data_as_tree_elements_operations_test(configuration):
        return ShouldTreesWithDataAsTreeElementsOperations(configuration)

    @staticmethod
    def retrieve_shouldtrees_data_as_tree_elements_exchange_operations_test(configuration):
        return ShouldTreesWithDataAsTreeElementsExchangeOperations(configuration)


