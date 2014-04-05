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

from PyQt4.QtCore import QString
from PyQt4.QtGui import QMessageBox
from src.modell.logger import logging
from src.modell.enumerations import CONFIG_ENUM
import src.gui.gui_snippets
import src.modell.importer
import os.path

def format_colored_text(configuration, text):
    """ Convert "\n" to <br/> for html output (for editor window e.g.)

    """
    text = text.replace("\n", "<br/>")

    for hightlight_color, highlight_text in \
            configuration.data[str(CONFIG_ENUM.highlight_text)]:
        logging.debug("format_colored_text. color=" + hightlight_color
                      + " text:" + highlight_text)
        text = text.replace(highlight_text, "<font color=\""
                            + hightlight_color + "\">" + highlight_text
                            + "</font>")
    return text

def build_colored_qstring_from_list(text, configuration):
    """ Produces an QString of the given str. Parts of the given text will be
    colored using html tags (highlighted text).
    @param text: str object with text that should be converted to the
        colored text
    @return: QString object with the colored text of the given str parameter

    """
    text_output = QString()
    for i in "".join(text).split("\n"):
        if len(i.strip()) > 0:
            text_output.append(format_colored_text(configuration, i + "\n"))

    return text_output

def open_last_opened_file_when_configured(configuration,
                                          main_window,
                                          tree_reference):
    """ Open the "lats opened filename" when selected in the configuration
    window
    @configuration: object of type Configuration
    @param main_window: change the title of this QMainWindow object
    @param tree_reference: reference of type Tree object

    """
    importer = src.modell.importer.TextImporter(configuration)
    last_file_name = configuration.data[str(CONFIG_ENUM.LastFilename)]
    if configuration.data[str(CONFIG_ENUM.StartWithLastFile)] == True \
            and last_file_name is not None and last_file_name != "":
        logging.debug("last file opened because of Option")
        logging.debug("filename: %s", last_file_name)

        if not os.path.isfile(last_file_name):
            logging.debug("last opened filename doesn't exist."
                          + " Stopping import.")
            QMessageBox.warning(main_window, "Warning",
                        '''Lastly opened file doesn't exist:'''
                        + last_file_name + ''' File won't be opened.''')
            return

        remainder_lines = importer.read_file(main_window.centralWidget(),
                                             last_file_name,
                                             tree_reference)
        change_window_title(last_file_name, main_window)

        src.gui.gui_snippets.ImportResult(main_window,
                     remainder_lines,
                     configuration)

def change_window_title(file_name, main_window):
    """ Changes the window title of the program.
    @param file_name: filename
    @param main_window: change the title of this QMainWindow object

    """
    file_name_if_exists = ""
    if file_name != "":
        file_name_if_exists = "File:" + file_name
    main_window.setWindowTitle("tree_editor V0.9.0 |" + file_name_if_exists)

