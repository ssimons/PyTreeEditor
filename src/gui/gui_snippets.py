#!/usr/bin/python
# -*- coding: utf-8*-
"""
Tree Editor.
Copyright (C) 2014  ssimons

    Contains small guis - like a helper module

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

import webbrowser
from PyQt4.QtGui import QDialog, QLineEdit, QGroupBox, QListWidgetItem, \
    QVBoxLayout, QTextEdit, QLabel, QPushButton
from PyQt4.Qt import QEvent, Qt
from PyQt4.QtCore import QObject, SIGNAL
import src.gui.gui_helper

class ImportResult(QDialog):
    """
    A small QDialog window to display the results of an import.
    Shows results/ignored file stuff in somewhat like an report window.
    """

    def __init__(self, parent, remainder_lines_list, configuration):
        """ Initializes the derived QDialog and builds up the GUI.
        @param parent: parent object to pass-through to the QDialog.
        @param remainder_lines_list: a (!) list with ignored lines - should
            be applied as string -
        @param configuration: Current Configuration object.

        """

        QDialog.__init__(self, parent)

        self.setModal(True)

        group_box_ignored = QGroupBox("Ignored")

        lab_delimiter_note = QLabel("Adjust your delimiter to reduce the "
                               + "ignored lines.\n Probably incorrect formatted"
                               + " lines were ignored.")

        text_output_ignored = QTextEdit()
        text_output_ignored.setWindowTitle("Ignored file data")
        text_output_ignored.setReadOnly(True)

        text_output_layout = QVBoxLayout()
        text_output_layout.addWidget(lab_delimiter_note)
        text_output_layout.addWidget(text_output_ignored)
        group_box_ignored.setLayout(text_output_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box_ignored)
        self.setLayout(main_layout)

        text_output_ignored.setHtml(
            src.gui.gui_helper.build_colored_qstring_from_list(
                remainder_lines_list, configuration))

        self.show()


class LineEditAcceptingTabulator(QLineEdit):
    """
    Derived class from QLineEdit which uses tabulator to add \t instead
    of trigger to loose the focus
    """

    def __init__(self, parent):
        """ Initializes the derived QLineEdit.
        @param parent: parent object to pass-through to the QLineEdit.

        """
        QLineEdit.__init__(self, parent)

    def event(self, event):
        """Pressing the tab key of keyboard will result in adding an \t
        to the text area.

        """
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.insert("\t")
            return True
        return QLineEdit.event(self, event)

class ListWidgetItemWithColor(QListWidgetItem):
    """
    Derived class from QListWidgetItem to save the highlight_color
    (which will be used for the icon)
    In the main class this color will be used to highlight text
    (the text of the current list item)
    @highlight_color may contain the full name like "black" or the
    color value containing of digits

    """

    def __init__(self):
        """ Constructor to initialize.

        """
        QListWidgetItem.__init__(self)
        self.highlight_color = "black"


class InfoLicenseWindow(QDialog):
    """
    A small QDialog window to display info and license of program.
    """
    LINK_TO_LICENSE = "http://www.gnu.org/licenses/gpl-2.0.txt"

    def __init__(self, parent):
        """ Initializes the derived QDialog and builds up the GUI.
        @param parent: parent object to pass-through to the QDialog.

        """

        QDialog.__init__(self, parent)

        self.setModal(True)

        group_box_ignored = QGroupBox("Info / License")

        label1 = QLabel("Tree editor")
        label2 = QLabel("Version: 0.9.0")
        label3 = QLabel("www.s-simons.de")
        label4 = QLabel("This program is a free software")
        label5 = QLabel("published under the GPL 2 license: ")
        show_button = QPushButton("Show license", self)
        QObject.connect(show_button,
                        SIGNAL('clicked()'),
                        lambda: webbrowser.open(self.LINK_TO_LICENSE, 1))

        text_output_layout = QVBoxLayout()
        text_output_layout.addWidget(label1)
        text_output_layout.addWidget(label2)
        text_output_layout.addWidget(label3)
        text_output_layout.addWidget(QLabel())
        text_output_layout.addWidget(label4)
        text_output_layout.addWidget(label5)
        text_output_layout.addWidget(show_button)
        group_box_ignored.setLayout(text_output_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box_ignored)
        self.setLayout(main_layout)

        self.show()
