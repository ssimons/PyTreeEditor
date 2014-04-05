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

from PyQt4.QtGui import QCheckBox, QFormLayout, QGroupBox, QDialog, \
    QLabel, QPushButton, QVBoxLayout, QWidget, QTabWidget, QMessageBox
from PyQt4.QtCore import QObject, SIGNAL
from src.modell.logger import logging
from src.gui.gui_snippets import LineEditAcceptingTabulator
from src.config.config_file import ConfigurationFileWriter
from src.modell.enumerations import CONFIG_ENUM
from src.gui.config.color_management import ColorChoosingWidget

class ConfigurationGUI(QDialog):
    """

    Class ConfigurationGUI uses PyQt elements to alter the current
    configuration.
    The gui is divided in profile specific gui elements (profile management,
    color management, input of delimiter) and main features (
    @author: ssimons

    """

    def __init__(self, parent, configuration):
        """ Initializes the derived QDialog and builds up the GUI.
            @param parent: parent object to pass-through to the QDialog.
            @param configuration: Configuration object to get the current
                configuration information

        """
        QDialog.__init__(self, parent)

        self._conf = configuration
        self.setModal(True)

        #define all instance attributes
        self.name_pre_sequence = LineEditAcceptingTabulator(self)
        self.name_first = LineEditAcceptingTabulator(self)
        self.name_second = LineEditAcceptingTabulator(self)
        self.name_second.setToolTip("Could be left empty.")
        self.checkbox_use_data_prefix = QCheckBox(
            "Are data lines characterized" + "by special characters as prefix?"
            + " Please note option below. "
            + "\nOtherwise every line not applying the above delimiter is a "
            + "data line.", self)
        self.name_data = LineEditAcceptingTabulator(self)
        self.checkbox_ignore_prefix = QCheckBox(
            "Do you want to ignore lines beginning with special characters? "
            + "Please note option below..", self)
        self.name_ignore_prefix = LineEditAcceptingTabulator(self)
        self.checkbox_data_expandable_in_tree = QCheckBox(
            "Data of tree element" + "expandable (as separate tree element)",
            self)
        self.checkbox_start_with_last_opened_file = QCheckBox(
            "Start program with recently opened file", self)

        self.color_choosing_widget = ColorChoosingWidget(self, self._conf)
        self.setLayout(self._init_gui_tab_and_groupbox_widgets())
        self._fill_gui_with_configuration_data()

        self.show()

    def _init_gui_tab_and_groupbox_widgets(self):
        #top area for main stuff
        group_box_main_config = QGroupBox("Configuration")
        main_config_layout = QFormLayout()

        widget_delimiter = self._init_gui_delimiter_entries()

        tab_widget = QTabWidget()
        tab_widget.addTab(widget_delimiter, "delimiter")
        tab_widget.addTab(self.color_choosing_widget, "colors")

        #widget for bottom = save button
        save_widget = QWidget()
        layout_save_widget = QFormLayout()
        save_button = QPushButton("save", self)
        QObject.connect(save_button, SIGNAL('clicked()'), self._save_config)
        layout_save_widget.addWidget(save_button)
        save_widget.setLayout(layout_save_widget)
        main_config_layout.addRow(self.checkbox_start_with_last_opened_file)
        group_box_main_config.setLayout(main_config_layout)
        tab_widget_layout = QVBoxLayout()
        tab_widget_layout.addWidget(group_box_main_config)
        tab_widget_layout.addWidget(tab_widget)
        tab_widget_layout.addWidget(save_widget)
        return tab_widget_layout

    def _init_gui_delimiter_entries(self):
        """Initialiase delimiters using the instance attributes of the
         __init__ function

        """
        widget_delimiter = QWidget()
        self.checkbox_ignore_prefix.setToolTip(
            "Probably you want to ignore "
            + "some line e.g. comments beginning with // or ;")
        self.checkbox_data_expandable_in_tree.setToolTip(
            "If this element is checked, every data line of its tree element "
            + "will be displayed as its own child tree element of the "
            + "current one. Otherwise the data will just be displayed as text "
            + "(e.g. in the text " + "area)")
        QObject.connect(self.checkbox_ignore_prefix,
                        SIGNAL('stateChanged(int)'),
                        self._checkbox_ignore_prefix_disables_textfield)
        QObject.connect(self.checkbox_use_data_prefix,
                        SIGNAL('stateChanged(int)'),
                        self._checkbox_use_data_prefix_disables_textfield)
        lab = QLabel("Delimiter. Please see the help to understand " \
                     + "the principle of these separators.")
        form_layout = QFormLayout()
        form_layout.addWidget(lab)
        form_layout.addRow("pre-sequence:", self.name_pre_sequence)
        form_layout.addRow("first delimiter:", self.name_first)
        form_layout.addRow("second delimiter:", self.name_second)
        form_layout.addRow(self.checkbox_use_data_prefix)
        form_layout.addRow("data :", self.name_data)
        form_layout.addRow(self.checkbox_ignore_prefix)
        form_layout.addRow("Ignore prefix:", self.name_ignore_prefix)
        form_layout.addRow(self.checkbox_data_expandable_in_tree)
        widget_delimiter.setLayout(form_layout)
        return widget_delimiter

    def _print_current_config(self):
        """
        Prints debug output of current configuration

        """
        logging.debug("Current config: pre_sequence: %s",
                      str(self._conf.data[str(CONFIG_ENUM.PreSequence)]))
        logging.debug("Current config: first_delimiter: %s",
                      str(self._conf.data[str(CONFIG_ENUM.FirstDelimiter)]))
        logging.debug("Current config: second_delimiter: %s",
                      str(self._conf.data[str(CONFIG_ENUM.SecondDelimiter)]))
        logging.debug("Current config: use_data_prefix: %s",
                      str(self._conf.data[str(CONFIG_ENUM.UseDataPrefix)]))
        logging.debug("Current config: data_delimiter: %s",
                      str(self._conf.data[str(CONFIG_ENUM.DataDelimiter)]))
        logging.debug("Current config: highlight_text: %s",
                      str(self._conf.data[str(CONFIG_ENUM.highlight_text)]))
        logging.debug("Current config: start_with_last_file: %s",
                      str(self._conf.data[str(CONFIG_ENUM.StartWithLastFile)]))
        logging.debug("Current config: last_filename: %s",
                      str(self._conf.data[str(CONFIG_ENUM.LastFilename)]))
        logging.debug("Current config: use_data_expandable_in_tree: %s",
                      str(self._conf.data[str(\
                          CONFIG_ENUM.UseDataExpandableInTree)]))
        logging.debug("Current config: use_ignore_prefix: %s",
                      str(self._conf.data[str(CONFIG_ENUM.UseIgnorePrefix)]))
        logging.debug("Current config: ignore_prefix: %s",
                      str(self._conf.data[str(CONFIG_ENUM.IgnorePrefix)]))

    def _fill_gui_with_configuration_data(self):
        """ produces a log of the current configuration values and
        pre-populates / fills the gui elements like checkboxes or input
        fields with the values of the configuration.

        """

        self._print_current_config()

        self.checkbox_start_with_last_opened_file.setChecked(
            bool(self._conf.data[str(CONFIG_ENUM.StartWithLastFile)]))
        self.name_pre_sequence.setText(\
            self._conf.data[str(CONFIG_ENUM.PreSequence)])
        self.name_first.setText(\
            self._conf.data[str(CONFIG_ENUM.FirstDelimiter)])
        self.name_second.setText(\
            self._conf.data[str(CONFIG_ENUM.SecondDelimiter)])
        self.checkbox_use_data_prefix.setChecked(\
            bool(self._conf.data[str(CONFIG_ENUM.UseDataPrefix)]))
        self.name_data.setText(self._conf.data[str(CONFIG_ENUM.DataDelimiter)])
        logging.info("should set dataexpandable val=%s  with bool=%s",
            str(self._conf.data[str(CONFIG_ENUM.UseDataExpandableInTree)]),
            str(bool(self._conf.data[
                str(CONFIG_ENUM.UseDataExpandableInTree)])))
        self.checkbox_data_expandable_in_tree.setChecked(
            bool(self._conf.data[str(CONFIG_ENUM.UseDataExpandableInTree)]))
        self.checkbox_ignore_prefix.setChecked(bool(
            self._conf.data[str(CONFIG_ENUM.UseIgnorePrefix)]))
        self._checkbox_ignore_prefix_disables_textfield()
        self._checkbox_use_data_prefix_disables_textfield()
        self.name_ignore_prefix.setText(\
            self._conf.data[str(CONFIG_ENUM.IgnorePrefix)])

        self.color_choosing_widget.fill_list_widget_of_color_elements()

    # ------------------------------------------------
    # -------------  Action functions---------------
    # ------------------------------------------------

    def _checkbox_ignore_prefix_disables_textfield(self):
        """Action function to enable/disable the text field of the str
        that indicates to ignore the line.

        """
        if self.checkbox_ignore_prefix.isChecked() == True:
            self.name_ignore_prefix.setDisabled(False)
        else:
            self.name_ignore_prefix.setDisabled(True)

    def _checkbox_use_data_prefix_disables_textfield(self):
        """Action function to enable/disable the text field of the str
        that indicates a data line

        """
        if self.checkbox_use_data_prefix.isChecked() == True:
            self.name_data.setDisabled(False)
        else:
            self.name_data.setDisabled(True)



    def _save_config(self):
        """ Transfers the values of the gui elements to the current
        configuration. Instanciates the ConfigurationFileReadWrite and writes
        the main and the process specific details to the config file.

        """

        if self.checkbox_ignore_prefix.isChecked() == True \
                and len(self.name_ignore_prefix.text()) == 0:
            QMessageBox.warning(self, "Warning: No ignore prefix",
                ''' Pleas enter an ignore prefix or deselect the checkbox.''')
            return


        #save color highlighting values
        self.color_choosing_widget.export_list_widget_to_config()

        self._conf.data[str(CONFIG_ENUM.PreSequence)] \
 = str(self.name_pre_sequence.text())
        self._conf.data[str(CONFIG_ENUM.FirstDelimiter)] \
 = str(self.name_first.text())
        self._conf.data[str(CONFIG_ENUM.SecondDelimiter)] \
 = str(self.name_second.text())
        self._conf.data[str(CONFIG_ENUM.DataDelimiter)] \
 = str(self.name_data.text())
        self._conf.data[str(CONFIG_ENUM.UseDataPrefix)] \
 = bool(self.checkbox_use_data_prefix.isChecked())
        self._conf.data[str(CONFIG_ENUM.UseDataExpandableInTree)] \
 = bool(self.checkbox_data_expandable_in_tree.isChecked())
        self._conf.data[str(CONFIG_ENUM.StartWithLastFile)] \
 = bool(self.checkbox_start_with_last_opened_file.isChecked())
        self._conf.data[str(CONFIG_ENUM.UseIgnorePrefix)] \
 = bool(self.checkbox_ignore_prefix.isChecked())
        self._conf.data[str(CONFIG_ENUM.IgnorePrefix)] \
 = str(self.name_ignore_prefix.text())

        try:
            ConfigurationFileWriter.write_config(self._conf)
        except IOError, exc:
            logging.exception(exc)
            QMessageBox.warning(self, "Critical",
                                ''' Configuratino couldn't be written to file.
                                Error:''' + exc.args[0])


        logging.debug("Save config from gui finished")

