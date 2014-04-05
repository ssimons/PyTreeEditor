#!/usr/bin/python
# -*- coding: utf-8*-

"""

Tree Editor.
Copyright (C) 2014  ssimons

    Adapted QT example to meet the needs of the project
    (redistribution).
    The Qt example is licensed under BSD (therefore the BSD license was added).
    example file: itemviews/editabletreemodel/treemodel.cpp

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

from PyQt4.QtCore import QAbstractItemModel, QVariant, Qt, QModelIndex
from PyQt4.QtCore import QString

class TreeModel(QAbstractItemModel):
    """ TreeModel is used as special data model of the tree view.
    It derives QAbstractItemModel from the Qt project to realise special
    functionality like displaying the label_name of the tree elements, showing
    their checked status (selected / not selected) and so on.

    """

    def __init__(self, tree_instance):
        """ Inititalizes tree model and super class.
        """
        QAbstractItemModel.__init__(self)
        self._treeRoot = tree_instance

        self._treeRoot.signal_tree_data_changed.connect(self.fire_model_changed)


    def _get_item(self, index):
        """ Interal function to retrieve appropriate tree element.
        """
        item = None
        if index.isValid():
            item = index.internalPointer()

        if item is not None:
            return item

        return self._treeRoot

    def parent(self, index):
        """ Overwrites parent function """
        if not index.isValid():
            return QModelIndex()

        parentItem = self._get_item(index).parent()

        if parentItem == self._treeRoot:
            return QModelIndex()

        return self.createIndex(
            parentItem.childs_index_of_parents_tree_element(),
            0,
            parentItem)

    def index(self, row, column, parent=QModelIndex()):
        """ Overwrites index function """
        try:
            if parent.isValid() and parent.column() != 0:
                return QModelIndex()
        except AttributeError:
            return QModelIndex()
        parentItem = self._get_item(parent)

        childItem = parentItem.children_at(row)
        if childItem is not None:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        """ Overwrites rowCount function """
        parentItem = self._get_item(parent)
        return parentItem.child_size()

    def columnCount(self, parent):
        """ Overwrites columnCount function """
        return 1

    def data(self, index, role=Qt.DisplayRole):
        """ Overwrites data function in order to to display the label_name of
        the tree element and the checked status (checked / not checked)
        """
        if not index.isValid():
            return QVariant()
        if  role != Qt.DisplayRole \
                and role != Qt.EditRole \
                and role != Qt.CheckStateRole:
            return QVariant()

        item = self._get_item(index)


        #checkbox before element
        if role == Qt.CheckStateRole:
            return self._check_state_from_item(item.check_state_bool())

        return item.label_name

    def _check_state_from_item(self, checked_info):
        """ Interal function to determine Qt Checked Status from boolean value.
        """
        if checked_info is True:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def headerData(self, section, orientation=Qt.Orientation, \
                   role=Qt.DisplayRole):
        """ Overwrites headerData function to display the file name in the first
        row of the tree widget.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QString(self._treeRoot.current_file_name)
        return QVariant()




    def setData(self, index=QModelIndex(), value=QVariant(), \
                role=Qt.CheckStateRole):
        """ Overwrites setData function in order to allow the elements to
        be checked and notifies listener.
        """
        if role == Qt.CheckStateRole:
            item = self._get_item(index)
            item.set_check_state_bool(not item.check_state_bool())
            self.dataChanged.emit(index, index)

        return False

    def flags(self, index=QModelIndex()):
        """ Overwrites flags function in order to allow the elements to
        be checked
        """
        if not index.isValid():
            return 0
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    def size(self):
        """ Returns child count of tree
        """
        return len(self._treeRoot)


    def fire_model_changed(self):
        """ Notifies the listener through signal that the model has changed
        """

        self.layoutChanged.emit()
