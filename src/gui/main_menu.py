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
import webbrowser
from PyQt4.QtGui import QFileDialog, QMenuBar, QMenu, QAction, QMessageBox, \
QInputDialog, QLineEdit
from PyQt4.QtCore import QObject, QDir, SIGNAL
from src.gui.config.configuration_gui import ConfigurationGUI
from src.config.config_file import ConfigurationFileWriter
from src.modell.logger import logging
from src.modell.importer import TextImporter
from src.modell.exporter import TextExporter
from src.modell.enumerations import CONFIG_ENUM
from src.gui.gui_snippets import ImportResult, InfoLicenseWindow
from src.modell import tree_operations
from src.gui import gui_helper
from src.modell.treestruct.tree_exceptions import \
    NoProperTreeElementException, NotEnoughTreeElementsCheckedException, \
    TreeElementsNotSameLevelException


class GuiMenu(QMenuBar):
    """

    Class GuiMenu contains the menu details incl. action functions that were
    moved out of main_menu module.

    @author: ssimons

    """
    HELP_WEBSITE_LINK = "http://www.s-simons.de/tree_editor_help.html"

    MAIN_TREE = True
    SECOND_TREE = False

    def __init__(self,
                 tree_main,
                 tree_second,
                 configuration,
                 right_window,
                 main_window,
                 signal_wrapper):
        """ Creates menu elements.
            @param tree_main: Tree object of main file / tree
                (left side)
            @param tree_second: Tree object of second file / tree
                (right side)
            @param text_output_instance: QTextEdit object which should be
                used / bind with the tree wiget.
            @param configuration: Current Configuration object.
            @param right_window: QWidget object of the second (right) file/tree
            @param main_window: QMainWindow object to change the title
            @param signal_wrapper: SignalWrapper object which wraps signals

        """
        QMenuBar.__init__(self, main_window.centralWidget())
        logging.info("menu foo")
        self.tree_main = tree_main
        self.tree_second = tree_second
        self._conf = configuration
        self.widget_right_window = right_window
        self.main_window = main_window
        self.signal_wrapper = signal_wrapper

        self.two_windows_action = QAction("Two Windows", self)
        self._importer = TextImporter(self._conf)

        self._init_gui_menu_view()
        self._init_gui_menu_main_file()
        self.menu_second_file = QMenu("SecondFile",
                                      self.main_window.centralWidget())
        self._init_gui_menu_second_file()

        gui_helper.change_window_title("", self.main_window)


    def _init_gui_menu_view(self):
        """Initialises the view menu ( with configuration, exit etc.)

        """
        menu1 = QMenu("View", self.main_window.centralWidget())

        self.two_windows_action.setCheckable(True)
        QObject.connect(self.two_windows_action,
                        SIGNAL('triggered()'),
                        self._show_or_hide_second_window_file)
        menu1.addAction(self.two_windows_action)

        configuration_gui_action = QAction("configuration", self)
        QObject.connect(configuration_gui_action,
                        SIGNAL('triggered()'),
                        self._gui_open_configuration)
        menu1.addAction(configuration_gui_action)
        info_license_action = QAction("Info/License", self)
        QObject.connect(info_license_action,
                        SIGNAL('triggered()'),
                        lambda: InfoLicenseWindow(self.main_window))
        menu1.addAction(info_license_action)
        help_gui_action = QAction("help", self)
        QObject.connect(help_gui_action,
                        SIGNAL('triggered()'),
                        lambda: webbrowser.open(self.HELP_WEBSITE_LINK, 1))
        menu1.addAction(help_gui_action)

        menu_exit_action = QAction("Exit", self)
        QObject.connect(menu_exit_action,
                        SIGNAL('triggered()'),
                        self._menu_exit)
        menu1.addSeparator()
        menu1.addAction(menu_exit_action)
        self.addMenu(menu1)
        logging.info("menu1" + str(menu1 is None))

    def _init_gui_menu_main_file(self):
        """Initialises the first window / file

        """
        menu_main_file = QMenu("MainFile", self.main_window.centralWidget())
        self.addMenu(menu_main_file)

        menu_open_main_file_action = QAction("Open file", self)
        QObject.connect(menu_open_main_file_action,
                        SIGNAL('triggered()'),
                        self._menu_main_window_open_file)
        menu_main_file.addAction(menu_open_main_file_action)

        menu_save_main_file_action = QAction("Save file", self)
        QObject.connect(menu_save_main_file_action,
                        SIGNAL('triggered()'),
                        self._default_file_save)
        menu_main_file.addAction(menu_save_main_file_action)

        remove_elem_in_main_file_action = QAction("Remove element", self)
        QObject.connect(remove_elem_in_main_file_action,
                        SIGNAL('triggered()'),
                        self._menu_delete_elem_main_file)
        menu_main_file.addAction(remove_elem_in_main_file_action)
        copy_main_to_second_file_action = QAction("Copy to second File", self)
        QObject.connect(copy_main_to_second_file_action,
                        SIGNAL('triggered()'),
                        self._menu_copy_main_to_second_file)
        menu_main_file.addAction(copy_main_to_second_file_action)

        expand_all_action = QAction("Expand all", self)
        QObject.connect(expand_all_action,
                        SIGNAL('triggered()'),
                        lambda: self.signal_wrapper. \
                            signal_treeview1_expand_all.emit())
        menu_main_file.addAction(expand_all_action)

        collapse_all_action = QAction("Collapse all", self)
        QObject.connect(collapse_all_action,
                        SIGNAL('triggered()'),
                        lambda: self.signal_wrapper. \
                            signal_treeview1_collapse_all.emit())

        menu_main_file.addAction(collapse_all_action)

        menu_main_file.addSeparator()
        self._initialize_tree_specific_menu_entries(self.tree_main,
                                                    menu_main_file,
                                                    self.MAIN_TREE)

    def _init_gui_menu_second_file(self):
        """Initialises the second window / file

        """
        self.menu_second_file.setEnabled(False)
        self.addMenu(self.menu_second_file)

        menu_open_second_file_action = QAction("Open file", self)
        QObject.connect(menu_open_second_file_action,
                        SIGNAL('triggered()'),
                        self._menu_second_window_open_file)
        self.menu_second_file.addAction(menu_open_second_file_action)
        remove_elem_in_second_file_action = QAction("Remove element", self)
        QObject.connect(remove_elem_in_second_file_action,
                        SIGNAL('triggered()'),
                        self._menu_delete_elem_second_file)
        self.menu_second_file.addAction(remove_elem_in_second_file_action)
        copy_second_to_main_file_action = QAction("Copy to main File", self)
        QObject.connect(copy_second_to_main_file_action,
                        SIGNAL('triggered()'),
                        self._menu_copy_second_to_main_file)
        self.menu_second_file.addAction(copy_second_to_main_file_action)

        expand_all_action = QAction("Expand all", self)
        QObject.connect(expand_all_action,
                        SIGNAL('triggered()'),
                        lambda: self.signal_wrapper. \
                            signal_treeview2_expand_all.emit())
        self.menu_second_file.addAction(expand_all_action)

        collapse_all_action = QAction("Collapse all", self)
        QObject.connect(collapse_all_action,
                        SIGNAL('triggered()'),
                        lambda: self.signal_wrapper. \
                            signal_treeview2_collapse_all.emit())
        self.menu_second_file.addAction(collapse_all_action)

        self.menu_second_file.addSeparator()
        self._initialize_tree_specific_menu_entries(self.tree_second,
                                                    self.menu_second_file,
                                                    self.SECOND_TREE)

    def _initialize_tree_specific_menu_entries(self,
                                               tree_instance,
                                               menu_reference,
                                               is_main_tree):
        """ Creates standard menu entries (that are used for both trees)
            for the given tree_instance
            @param tree_instance: Tree object that
                should be used.
            @param menu_reference: QMenu object where to add the menu entries
            @param is_main_tree: to differ between main and second tree.

        """

        exchange_action = QAction("Exchange", self)
        QObject.connect(
            exchange_action,
            SIGNAL('triggered()'),
            lambda: self._menu_exchange_tree_elements(tree_instance))

        menu_reference.addAction(exchange_action)

        data_up_action = QAction("DataUp", self)
        QObject.connect(
            data_up_action,
            SIGNAL('triggered()'),
            #call data up move
            lambda: QMessageBox.information(self.main_window, "Info",
                        '''The following were susscessully moved up: '''
                        + "".join(tree_operations.data_up_move(tree_instance))))
        menu_reference.addAction(data_up_action)

        data_down_action = QAction("DataDown", self)
        QObject.connect(
            data_down_action,
            SIGNAL('triggered()'),
            #call data down move
            lambda: QMessageBox.information(self.main_window, "Info",
                        '''The following were successfully moved down: '''
                        + "".join(tree_operations.data_down_move(tree_instance)
                        )))

        menu_reference.addAction(data_down_action)

        data_replace_action = QAction("Replace", self)
        QObject.connect(
            data_replace_action,
            SIGNAL('triggered()'),
            lambda: self._menu_change_label_of_selected_elements(tree_instance,
                                                                 is_main_tree))
        menu_reference.addAction(data_replace_action)

        data_search_and_replace_action = QAction("Search and replace", self)
        QObject.connect(
            data_search_and_replace_action,
            SIGNAL('triggered()'),
            lambda: tree_operations.data_search_and_replace(self.main_window,
                                                  tree_instance))
        menu_reference.addAction(data_search_and_replace_action)
        data_search_and_replace_action.setEnabled(False)



    # ------------------------------------------------
    # -------------  MENU ACTIONS --------------------
    # ------------------------------------------------

    def _default_file_save(self):
        """ Action function to save to file.

        """

        file_name = QFileDialog.getSaveFileName(self,
                                       "Save file",
                                       QDir.home().dirName(),
                                       "All files (*.*)")
        if not file_name.isNull():
            _exporter = TextExporter(self._conf)
            _exporter.write_file_from_data(self.tree_main,
                                           file_name)
            QMessageBox.information(self.main_window, "Info",
                '''Please ensure the correctness of the output file by
                comparing (diff) the output file to the original one. See
                help for further information.''')

    def _show_or_hide_second_window_file(self):
        """ Action function to show/hide the second window (which means the
        second pair of tree and text editor).

        """
        if self.two_windows_action.isChecked():
            self.widget_right_window.show()
            self.main_window.resize(self.main_window.width() * 2,
                                    self.main_window.height())
            self.menu_second_file.setEnabled(True)
        else:
            self.widget_right_window.hide()
            self.main_window.resize(self.main_window.width() / 2,
                                    self.main_window.height())
            self.menu_second_file.setEnabled(False)

    def _gui_open_configuration(self):
        """ Action to open the configuration window.

        """
        configuration_gui = ConfigurationGUI(self,
                                             self._conf)
        configuration_gui.show()

    def _menu_change_label_of_selected_elements(self, tree_instance,
                                                is_main_tree):
        text, ok_response = QInputDialog.getText(self.main_window, "Replace",
            "Replace checked to:", QLineEdit.Normal, QDir.home().dirName())
        logging.debug("Replace / Change label with:" + text)
        if ok_response is False:
            return

        result_list = tree_operations.tree_element_change_label(tree_instance,
                                                                text)

        #emit the signal to trigger a click event. That is needed to refresh
        #the texteditor, that it contains the replaced data.
        if is_main_tree == self.SECOND_TREE:
            self.signal_wrapper.signal_treeview2_clicked.emit()
        else:
            self.signal_wrapper.signal_treeview1_clicked.emit()


        QMessageBox.information(self.main_window, "Info",
            '''The labels of the following tree elements were
            successfully renamned/changed : '''
            + "".join(result_list))

    def _menu_exchange_tree_elements(self, tree_instance):
        """ Action to exchange (data) tree elements.

        """
        try:
            tree_operations.exchange_elements(tree_instance)
        except NotEnoughTreeElementsCheckedException as netc:
            QMessageBox.warning(self.main_window, "Warning", netc.args[0])
            return
        except NoProperTreeElementException as npte:
            QMessageBox.warning(self.main_window, "Warning", npte.args[0])
            return
        except TreeElementsNotSameLevelException as tnl:
            QMessageBox.information(self.main_window, "Info", tnl.args[0])
            return


    def _menu_exit(self):
        """ Action to exit the program.

        """
        try:
            ConfigurationFileWriter.write_config(self._conf)
        except IOError, exc:
            logging.exception(exc)
        logging.shutdown()
        sys.exit()

    def _menu_main_window_open_file(self):
        """ Action to open a file in the main window.
        Used the QFileDialog to open the file.

        """
        #clear old list/tree
        self.tree_main.clear()
        self.signal_wrapper.signal_editor_of_tree1_clear.emit()

        file_name = QFileDialog.getOpenFileName(self,
                                               "Open file",
                                               QDir.home().dirName(),
                                               "All files (*.*)")
        logging.debug("_menu_main_window_open_file" + file_name)
        if not file_name.isNull():
            remainder_lines = self._importer.read_file(
                self.main_window.centralWidget(), file_name, self.tree_main)
            self._conf.data[str(CONFIG_ENUM.LastFilename)] = str(file_name)
            try:
                ConfigurationFileWriter.write_config(self._conf)
            except IOError, exc:
                logging.exception(exc)
                QMessageBox.warning(self, "Critical",
                    ''' Configuratino couldn't be written to file.
                    Error:''' + exc.args[0])
            gui_helper.change_window_title(file_name, self.main_window)

            ImportResult(self.main_window,
                         remainder_lines,
                         self._conf)


    def _menu_second_window_open_file(self):
        """ Action to open a file in the second window/file.
        Used the QFileDialog to open the file.

        """
        #clear old list/tree
        self.tree_second.clear()
        self.signal_wrapper.signal_editor_of_tree2_clear.emit()

        file_name = QFileDialog.getOpenFileName(self,
                                               "Open file",
                                               QDir.home().dirName(),
                                               "All files (*.*)")
        if not file_name.isNull():
            remainder_lines = self._importer.read_file(
                self.main_window.centralWidget(), file_name, self.tree_second)

            ImportResult(self.main_window,
                         remainder_lines,
                         self._conf)


    def _menu_delete_elem_main_file(self):
        """ Action to delete selected tree elements in the main file/tree.
        Selected means that the checkboxes of the tree element is checked.

        """
        failed_elements \
 = tree_operations.remove_element_is_from_tree(self.tree_main)
        failed_elems_string = "".join(failed_elements)
        if failed_elems_string != "":
            QMessageBox.warning(self.main_window, "Warning",
                                failed_elems_string + ''' cannot be deleted.
                                Check the log.''')


    def _menu_delete_elem_second_file(self):
        """ Action to delete selected tree elements in the second file/tree.
        Selected means that the checkboxes of the tree element is checked.

        """
        failed_elements \
 = tree_operations.remove_element_is_from_tree(self.tree_second)
        failed_elems_string = "".join(failed_elements)
        if failed_elems_string != "":
            QMessageBox.warning(self.main_window, "Warning",
                                failed_elems_string + ''' cannot be deleted.
                                Check the log.''')



    def _menu_copy_main_to_second_file(self):
        """ Action function to copy elements from main tree (file) to the
        second tree (file).

        """
        remainder_lines = \
            tree_operations.copy_elements_to_other_tree(
                self.tree_main, self.tree_second, self._conf)
        ImportResult(self.main_window, remainder_lines, self._conf)

    def _menu_copy_second_to_main_file(self):
        """ Action function to copy elements from second tree (file) to the
        main tree (file).

        """
        remainder_lines = \
            tree_operations.copy_elements_to_other_tree(
                self.tree_second, self.tree_main, self._conf)
        ImportResult(self.main_window, remainder_lines, self._conf)
