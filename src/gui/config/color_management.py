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

from PyQt4.QtGui import QColor, \
    QHBoxLayout, QIcon, QInputDialog, QDialog, QMessageBox, \
    QLineEdit, QLabel, QListWidget, QPixmap, QPushButton, \
    QColorDialog, QVBoxLayout, QWidget
from PyQt4.QtCore import QDir, QObject, SIGNAL
from src.modell.logger import logging
from src.gui.gui_snippets import ListWidgetItemWithColor
from src.modell.enumerations import CONFIG_ENUM

class ColorChoosingWidget(QWidget):
    """

    Class ColorChoosingWidget uses PyQt to build gui details for the color
    management. It was moved from the config_gui module.
    @author: ssimons

    """

    def __init__(self, parent, configuration):
        """ Initializes the derived QWidget and builds up the GUI.
            @param parent: parent object to pass-through to the QWidget.
            @param configuration: Configuration object to get the current
                configuration informations

        """
        QWidget.__init__(self, parent)
        self._conf = configuration

        self.list_widget = QListWidget(self)
        lab_colors_note = QLabel("Define Elements for text highlighting:")

        widget_color_buttons = QWidget()
        layout_color_buttons = QHBoxLayout()

        color_new_button = QPushButton("New", self)
        QObject.connect(color_new_button,
                        SIGNAL('clicked()'),
                        self._list_widget_new)
        layout_color_buttons.addWidget(color_new_button)

        color_delete_button = QPushButton("Delete", self)
        QObject.connect(color_delete_button,
                        SIGNAL('clicked()'),
                        self._list_widget_delete)
        layout_color_buttons.addWidget(color_delete_button)

        color_change_color_button = QPushButton("Change color", self)
        QObject.connect(color_change_color_button,
                        SIGNAL('clicked()'),
                        self._list_widget_change_color)
        layout_color_buttons.addWidget(color_change_color_button)

        color_change_text_button = QPushButton("Change text", self)
        QObject.connect(color_change_text_button,
                        SIGNAL('clicked()'),
                        self._list_widget_change_text)
        layout_color_buttons.addWidget(color_change_text_button)
        widget_color_buttons.setLayout(layout_color_buttons)

        layout_color_buttons_and_list = QVBoxLayout()
        layout_color_buttons_and_list.addWidget(widget_color_buttons)
        layout_color_buttons_and_list.addWidget(lab_colors_note)
        layout_color_buttons_and_list.addWidget(self.list_widget)
        self.setLayout(layout_color_buttons_and_list)

    def get_list_widget(self):
        """ Returns a reference of the QListWidget object

        """
        return self.list_widget

    # ------------------------------------------------
    # -------------  Action functions---------------
    # ------------------------------------------------

    def _list_widget_new(self):
        """Action function to add a new element to the list widget of colors.

        """
        text, ok_response = QInputDialog.getText(self, "New Text",
                                          "Highlighted text:", QLineEdit.Normal,
                                          QDir.home().dirName())
        if ok_response is True:
            new_item = ListWidgetItemWithColor()
            new_item.setText(text)
            new_item.highlight_color = "black"
            pixmap_black_temp = QPixmap(100, 100)
            pixmap_black_temp.fill(QColor(new_item.highlight_color))
            icon_black_temp = QIcon(pixmap_black_temp)
            new_item.setIcon(icon_black_temp)
            self.list_widget.addItem(new_item)

    def _list_widget_delete(self):
        """Action function to delete an element of the list widget of colors.

        """
        if self.list_widget.currentItem() is not None:
            self.list_widget.takeItem(self.list_widget.currentRow())
        else:
            QMessageBox.warning(self, "Warning",
            ''' No element selected.''')

    def _list_widget_change_color(self):
        """Action function to change the color of an selected element in the
        list widget of colors. An color dialog opens to let the user choose
        an color.

        """
        if self.list_widget.currentItem() is not None:
            current_elem = self.list_widget.currentItem()

            pick = QColorDialog(self)
            if pick.exec_() == QDialog.Accepted:
                color = pick.selectedColor().name()
                current_elem.highlight_color = color
                pixmap_temp = QPixmap(100, 100)
                pixmap_temp.fill(QColor(current_elem.highlight_color))
                temp_icon = QIcon(pixmap_temp)
                current_elem.setIcon(temp_icon)
        else:
            QMessageBox.warning(self, "Warning",
            ''' No element selected.''')

    def _list_widget_change_text(self):
        """Action function to change the text of an selected element in the
        list widget of colors. An input dialog opens to let the user choose
        another text.

        """
        if self.list_widget.currentItem() is not None:
            current_elem = self.list_widget.currentItem()

            ok_response = False
            text, ok_response = QInputDialog.getText(self,
                "Change Text", "Highlighted text:", QLineEdit.Normal,
                QDir.home().dirName())
            if ok_response is True:
                current_elem.setText(text)
        else:
            QMessageBox.warning(self, "Warning",
            ''' No element selected.''')

    def fill_list_widget_of_color_elements(self):
        """Adds the color-text-pairs from the configuration to the list_widget
        """
        for hightlight_color, highlight_text in  \
                self._conf.data[str(CONFIG_ENUM.highlight_text)]:
            logging.debug("adding highlight eleme from configuration." +
                          "color=%s text:%s",
                          hightlight_color,
                          highlight_text)
            new_item = ListWidgetItemWithColor()
            new_item.setText(highlight_text)
            new_item.highlight_color = hightlight_color
            pixmap_temp = QPixmap(100, 100)
            pixmap_temp.fill(QColor(new_item.highlight_color))
            icon_temp = QIcon(pixmap_temp)
            new_item.setIcon(icon_temp)
            self.list_widget.addItem(new_item)


    def export_list_widget_to_config(self):
        self._conf.data[str(CONFIG_ENUM.highlight_text)] = []
        for i in range(self.list_widget.count()):
            listitem = self.list_widget.item(i)
            logging.debug("save highlight-elem. color: %s text:%s",
                          str(listitem.highlight_color),
                          listitem.text())
            self._conf.data[str(CONFIG_ENUM.highlight_text)].append(
                [str(listitem.highlight_color), str(listitem.text())])
