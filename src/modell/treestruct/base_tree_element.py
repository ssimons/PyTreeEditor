#!/usr/bin/python
# -*- coding: utf-8*-

"""

Tree Editor.
Copyright (C) 2014  ssimons

    Inspired by the example of Qt (redistribution).
    Therefore the BSD license might be necessary.
    Example file: itemviews/editabletreemodel/treeitem.cpp

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

#****************************************************************************
#**
##** Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
#** Contact: http://www.qt-project.org/legal
#**
#** This file is part of the examples of the Qt Toolkit.
#**
#** $QT_BEGIN_LICENSE:BSD$
#** You may use this file under the terms of the BSD license as follows:
#**
#** "Redistribution and use in source and binary forms, with or without
#** modification, are permitted provided that the following conditions are
#** met:
#**   * Redistributions of source code must retain the above copyright
#**     notice, this list of conditions and the following disclaimer.
#**   * Redistributions in binary form must reproduce the above copyright
#**     notice, this list of conditions and the following disclaimer in
#**     the documentation and/or other materials provided with the
#**     distribution.
#**   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
#**     of its contributors may be used to endorse or promote products derived
#**     from this software without specific prior written permission.
#**
#**
#** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
#**
#** $QT_END_LICENSE$
#**
#****************************************************************************/

from PyQt4.QtCore import QObject
from src.modell.treestruct.tree_exceptions import \
    ChildrenAlreadyExistsException, ChildrenDoesntExistsException, \
    IndexOutOfBoundsException
class BaseTreeElement(QObject):
    """Abstract implementation for Tree and TreeElemeent.
    Derives QObject to let Tree ( a derived class) use signals.
    """

    def __init__(self):
        """ Initializes BaseTreeElement and QObject.
        Additionally attributes are initialized
        """
        super(BaseTreeElement, self).__init__()
        self.children = []
        self.label_name = str()
        self.parent_element = None
        self.check_state = False

    def add_children_without_modelnotify(self, new_children):
        """A new TreeElement object (derived from BaseTreeElement) will be
        added to this tree. The model won't be notified of this change.
        """
        if new_children not in self.children:
            self.children.append(new_children)
        else:
            raise ChildrenAlreadyExistsException("Cannot add element " \
                                                 + new_children.label_name)

    def add_children_at_without_modelnotify(self, position, new_children):
        """A new TreeElement object (derived from BaseTreeElement) will be
        added at the appropriate position. An IndexOutOfBoundsException will be
        raised if the given position isn't valid.
        The model won't be notified of this change.
        """
        if position < 0 or position > self.child_size():
            raise IndexOutOfBoundsException("Cannot add element at position" \
                                            + str(position))

        self.children.insert(position, new_children)


    def parent(self):
        return self.parent_element

    def childs_index_of_parents_tree_element(self):
        """ Returns the position in the children list of the parent tree.
        """
        current_parent_element = self.parent()
        if current_parent_element is not None:
            return current_parent_element.children.index(self)
        return 0

    def remove_children_without_modelnotify(self, deleting_children):
        """The given TreeElement object (derived from BaseTreeElement) will be
        removed from the current tree. An ChildrenDoesntExistsException will be
        raised if given tree element doesn't exist in the current tree.
        The model won't be notified of this change.
        """
        if deleting_children in self.children:
            self.children.remove(deleting_children)
        else:
            raise ChildrenDoesntExistsException("Cannot delete element " \
                                                + deleting_children.label_name)

    def get_children(self):
        """Returns children of this tree.
        """
        return self.children

    def has_children(self):
        """Returns True if the current tree has children (size > 0)
        """
        return self.child_size() > 0

    def child_size(self):
        """Returns how much children the current tree has.
        """
        return len(self.children)

    def children_at(self, index):
        """Returns the children at the given index. Raises
        IndexOutOfBoundsException for invalid index values.
        @param index: number of the index to be returned
        @return: TreeElement object (derived from BaseTreeElement) at the given
            index
        @raise IndexOutOfBoundsException: when the given index isn' valid
        """

        size = len(self.children)
        if index >= size:
            raise IndexOutOfBoundsException(str(index) \
                + " is >= size (" + str(size) + ")")
        return self.children[index]

    def row(self):
        """Needed for tree model
        """
        return 1

    def check_state_bool(self):
        """Returns the check state (whether current tree element is checked or
        not)"""
        return self.check_state

    def set_check_state_bool(self, bool_value):
        """Sets the check state of the current tree element (whether tree
        element is checked or not)"""
        self.check_state = bool_value

