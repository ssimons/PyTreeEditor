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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

"""
from src.modell.logger import logging
from src.modell.enumerations import TREE_LEVEL_ENUM, CONFIG_ENUM
from PyQt4.QtCore import pyqtSignal
from src.modell.treestruct.base_tree_element import BaseTreeElement


class Tree(BaseTreeElement):
    """
    The signal will be connected to the TreeModel. Every time the signal
    triggers the TreeModel - it will itself trigger the TreeView object to
    refresh the GUI.
    """
    signal_tree_data_changed = pyqtSignal()

    def __init__(self, configuration):
        """ Initializes the derived BaseTreeElement.
        @param configuration: Configuration object to get the current
            configuration information

        """
        BaseTreeElement.__init__(self)
        self._conf = configuration

        # Order of the original main-tree-elemens of input file.
        # This informtion will be used to keep the initial order
        # when writing to the file again.
        self.order_of_elements_references = []

        self.current_file_name = str()

    def get_root_elements(self):
        """ Returns a list of all root elements - the tree elements of
        the highest level.
        @return: a list of root elements
        """
        return self.get_children()


    def clear(self):
        """ Clears tree and the corresponding list
        Notifies that data has changed.
        """

        del self.order_of_elements_references[:]

        #delete all childs
        for element in self.get_children():
            element.clear()
        del self.get_children()[:]
        self.fire_data_changed()

    def set_file_name(self, file_name):
        """ Sets the file name to be displayed using the tree model
        """
        self.current_file_name = file_name


    def fire_data_changed(self):
        """ Notifies the listener (in this case the tree model) through signal
        that the model has changed.
        """
        logging.debug("fire_data_changed of tree_element")
        self.signal_tree_data_changed.emit()




class TreeElement(BaseTreeElement):
    """
    Derived class from BaseTreeElement to enrich the tree element with
    other information like label_name(name), line_data and level information.

    """


    def __init__(self, label_name, tree_level, parent_element):
        """ Initializes the derived BaseTreeElement and hold the label_name
        reference and the tree level information of the element. Additionally
        a line_data representation (type str) is initialized which remembers
        the str representation of the tree element.

        @param label_name: str object which text should be displayed for the
            tree element
        @param tree_level: TREE_LEVEL_ENUM object that the element
            knows its own level.
        @param parent_element: parent object to pass-through to the QLineEdit.
        """
        BaseTreeElement.__init__(self)
        self.label_name = label_name
        self.tree_level = tree_level
        self.parent_element = parent_element
        self.line_data = str()



    def __str__(self):
        return  str(self.label_name) \
            + " " + str(self.tree_level)
    def clear(self):
        """ Deletes all children and its children.
        """ 
        for element in self.get_children():
            element.clear()
        del self.get_children()[:]

    def parent(self):
        return self.parent_element


    def add_line_data(self, new_line):
        """ Append strings to the line_data attribute.
        @param new_line: str to add to the data representation.

        """
        self.line_data += new_line

    def change_label(self, label_new):
        """ Replaces the current label_name information of the current
        element to the given one.
        When the current label_name is an data element it should also add an
        new_line (\n)
        @param label_new: new name as str

        """
        self.label_name = label_new

    def remove_this_element(self):
        """ Remove this (self) element.

        """
        logging.debug("remove_element " + self.label_name + " at level "
                      + str(self.tree_level) + "parent=?"
                      + str(self.parent() is not None))
        if self.parent() is not None:
            self.parent().remove_children_without_modelnotify(self)

    def get_line_data_elements_to_write_file(self, configuration):
        """ Retrieves information of the current element in the following
        order as list:
        (data, (all existing) parent-labels, current label_name)
        These informations are required to build a complete line of this
        element param configuration  current Configuration object
        @param configuration: Configuration object to gett the current
            configuration informations
        @return: a list of elements - see text above.

        """
        main_identifier_line_elems = []

        current_element = self
        #use parent element if the current one is a data element (expanded)
        if self.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED:
            current_element = self.parent()

        #Differ between data as text (first one) and data as tree
        #nodes (else case)
        if configuration.data[str(CONFIG_ENUM.UseDataExpandableInTree)] \
                is False:
            main_identifier_line_elems.append(current_element.line_data)
        else:
            str_childs = []
            for i in range(current_element.child_size()):
                if current_element.children_at(i).tree_level \
                        == TREE_LEVEL_ENUM.DATA_EXPANDED:
                    if configuration.data[str(CONFIG_ENUM.UseDataPrefix)] \
                            is True:
                        str_childs.append(\
                            configuration.data[str(CONFIG_ENUM.DataDelimiter)])
                    str_childs.append(\
                        str(current_element.children_at(i).label_name))
                    str_childs.append("\n")
            main_identifier_line_elems.append("".join(str_childs))


        if current_element.tree_level == TREE_LEVEL_ENUM.CHILD_OF_CHILD:
            main_identifier_line_elems.append(
                current_element.parent().parent().label_name)
            main_identifier_line_elems.append(
                current_element.parent().label_name)
        if current_element.tree_level == TREE_LEVEL_ENUM.CHILD:
            main_identifier_line_elems.append(
                current_element.parent().label_name)

        main_identifier_line_elems.append(current_element.label_name)
        logging.debug("treeElement.get_line_data_elements_to_write_file: %s",
                      "".join(main_identifier_line_elems))
        return main_identifier_line_elems


