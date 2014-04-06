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

import sys
import os.path
from PyQt4.QtGui import QMainWindow, QHBoxLayout, QVBoxLayout, \
    QApplication, QTextEdit, QSplitter, QWidget, QTreeView, QMessageBox
from PyQt4.QtCore import QString, QModelIndex, QObject, pyqtSignal
from src.config.config_file import ConfigurationFileReader
from src.config.configuration import Configuration
from src.modell import tree_operations
from src.gui.main_menu import GuiMenu
from src.modell.logger import logging
from src.modell.treestruct.tree_element import Tree
from src.gui.tree_model import TreeModel
from src.gui import gui_helper

class MainGUI(QObject):
    """
    Class MainGUI uses PyQt elements to build up the main gui with all the
    gui elements of trees, editors, menu and so on.

    @author: ssimons

    """
    MAIN_TREE = True
    SECOND_TREE = False

    signal_treeview1_expand_all = pyqtSignal()
    signal_treeview2_expand_all = pyqtSignal()
    signal_treeview1_collapse_all = pyqtSignal()
    signal_treeview2_collapse_all = pyqtSignal()
    signal_treeview1_clicked = pyqtSignal()
    signal_treeview2_clicked = pyqtSignal()
    signal_editor_of_tree1_clear = pyqtSignal()
    signal_editor_of_tree2_clear = pyqtSignal()

    def __init__(self):
        """ Initializes the gui elements

        """
        super(MainGUI, self).__init__()
        app = QApplication(sys.argv)
        self.window = QWidget()

        self._conf = self._config_read_config_from_file_or_new()


        self.text_output_1 = QTextEdit()
        self.text_output_1_string = QString()
        self.text_output_2 = QTextEdit()
        self.text_output_2_string = QString()
        self.widget_right_window = QWidget()
        self.main_window = QMainWindow()
        self.tree_main = Tree(self._conf)
        self.tree_model_main = TreeModel(self.tree_main)

        self.tree_second = Tree(self._conf)
        self.tree_model_second = TreeModel(self.tree_second)
        self._init_gui()

        self.gui_menu = GuiMenu(self. tree_main,
                            self.tree_second,
                            self._conf,
                            self.widget_right_window,
                            self.main_window,
                            SignalWrapper(self.signal_treeview1_expand_all,
                                          self.signal_treeview2_expand_all,
                                          self.signal_treeview1_collapse_all,
                                          self.signal_treeview2_collapse_all,
                                          self.signal_treeview1_clicked,
                                          self.signal_treeview2_clicked,
                                          self.signal_editor_of_tree1_clear,
                                          self.signal_editor_of_tree2_clear))


        self.main_window.setMenuBar(self.gui_menu)



        gui_helper.open_last_opened_file_when_configured(self._conf,
                                                        self.main_window,
                                                        self.tree_main)
        self.main_window.show()
        app.exec_()

    def _init_gui(self):
        """ Initializes some widgets and delegates tree initializing to
        another function
        """
        self.text_output_1.setWindowTitle("Output Tree1")
        self.text_output_1.setReadOnly(True)
        self.text_output_2.setWindowTitle("Output Tree2")
        self.text_output_2.setReadOnly(True)
        self.signal_editor_of_tree1_clear.connect(self.text_output_1.clear)
        self.signal_editor_of_tree2_clear.connect(self.text_output_2.clear)

        self.main_window.setCentralWidget(self.window)
        self.main_window.resize(500, 300)

        widget_left_window = QWidget()
        widget_left_window.setLayout(
            self._initialize_create_tree(self.MAIN_TREE,
                                         self.tree_model_main,
                                         self.text_output_1))

        self.widget_right_window.setLayout(
            self._initialize_create_tree(self.SECOND_TREE,
                                         self.tree_model_second,
                                         self.text_output_2))
        self.widget_right_window.hide()

        widget_two_windows = QSplitter()
        layout_two_windows = QHBoxLayout()
        layout_two_windows.addWidget(widget_left_window)
        layout_two_windows.addWidget(self.widget_right_window)
        widget_two_windows.setLayout(layout_two_windows)
        self.window.setLayout(layout_two_windows)




    def _initialize_create_tree(self, is_main_tree,
                                      tree_model_instance,
                                      text_output_instance):
        """ Creates gui elements for the tree-gui given as parameter.
            Also binds the given text output to this tree.
            Will be used for both tree widgets.
            @param is_main_tree: to differ between main and second tree.
            @param tree_model_instance: TreeModel object that
                should be used.
            @param text_output_instance: QTextEdit object which should be
                used / bind with the tree wiget.

        """
        widget_tree_and_editor = QSplitter()
        layout_tree_and_editor = QHBoxLayout()

        tree_view = QTreeView()
        tree_view.setModel(tree_model_instance)

        tree_view.clicked[QModelIndex].connect(
            lambda: self.tree_element_clicked_event(is_main_tree))

        if is_main_tree == self.SECOND_TREE:
            self.signal_treeview2_expand_all.connect(tree_view.expandAll)
            self.signal_treeview2_collapse_all.connect(tree_view.collapseAll)
            self.signal_treeview2_clicked.connect(
                lambda: tree_view.clicked.emit(QModelIndex()))
        else:
            self.signal_treeview1_expand_all.connect(tree_view.expandAll)
            self.signal_treeview1_collapse_all.connect(tree_view.collapseAll)
            self.signal_treeview1_clicked.connect(
                lambda: tree_view.clicked.emit(QModelIndex()))

        layout_tree_and_editor.addWidget(tree_view)
        layout_tree_and_editor.addWidget(text_output_instance)
        widget_tree_and_editor.setLayout(layout_tree_and_editor)

        layout_window = QVBoxLayout()
        layout_window.addWidget(widget_tree_and_editor)
        return layout_window

    def tree_element_clicked_event(self, is_main_tree):
        """ Action to display information of all selected tree elements in the
        text area.  Selected means that the checkboxes of the tree element is
        checked.
        @param is_main_tree: to differ between main and second tree.

        """
        if is_main_tree == self.SECOND_TREE:
            tree_operations.show_data_text_of_checked_tree_elements(
                self.tree_second.get_root_elements(),
                self._conf,
                self.text_output_2,
                self.text_output_2_string)
        else:
            tree_operations.show_data_text_of_checked_tree_elements(
                self.tree_main.get_root_elements(),
                self._conf,
                self.text_output_1,
                self.text_output_1_string)
    def _config_read_config_from_file_or_new(self):
        """Opens configuration from file - or if isn't possible return a new
        one"""

        config_filename = Configuration.CONFIG_FILENAME

        if not os.path.isfile(config_filename):
            logging.debug("configuration file %s doesn't exist.",
                          config_filename)
            QMessageBox.information(self.window, "Info",
                        '''No configuration file ('''
                        + config_filename + ''') found. The default configuration is 
                        used. Change it in the configuration window (see menu 
                        View - Help). Afterwards a text file should be opened 
                        (menu MainFile - Open file).''')
            return Configuration()
        try:
            #try to open saved configuration and use it
            conf = Configuration()
            conf.data = ConfigurationFileReader.read_config()
            return conf
        except IOError, exc:
            logging.info("Couldn't open configuration file. "
                         + config_filename
                         + "Use the default values.")
            logging.exception(exc)
            return Configuration()



class SignalWrapper(object):
    """ Wraps some signals to use it in another class

    """
    def __init__(self,
                 signal_treeview1_expand_all,
                 signal_treeview2_expand_all,
                 signal_treeview1_collapse_all,
                 signal_treeview2_collapse_all,
                 signal_treeview1_clicked,
                 signal_treeview2_clicked,
                 signal_editor_of_tree1_clear,
                 signal_editor_of_tree2_clear):
        self.signal_treeview1_expand_all = signal_treeview1_expand_all
        self.signal_treeview2_expand_all = signal_treeview2_expand_all
        self.signal_treeview1_collapse_all = signal_treeview1_collapse_all
        self.signal_treeview2_collapse_all = signal_treeview2_collapse_all
        self.signal_treeview1_clicked = signal_treeview1_clicked
        self.signal_treeview2_clicked = signal_treeview2_clicked
        self.signal_editor_of_tree1_clear = signal_editor_of_tree1_clear
        self.signal_editor_of_tree2_clear = signal_editor_of_tree2_clear

