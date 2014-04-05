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

from src.modell.logger import logging
import io
import json
from src.config.configuration import Configuration


class ConfigurationFileWriter(object):
    """

    Class ConfigurationFileWriter provides access to the configuration
    file. It was realised using an matrix of dictionaries (two dimensions).
    Data format: JSON.
    The function write_config() is used to write the configuration in the
    recently explained data structue to a file.

    @author: ssimons

    """

    def __init__(self):
        pass

    @staticmethod
    def write_config(configuration):
        """ Writes the current configuraiton of the given object to the file.

        @param configuration: current Configuration object of whom the main
            details will be extracted to write to file
        @raise IOError: If file couldn't be written, an IOError will be raised.

        """
        logging.debug("write_config - start")
        with io.open(configuration.CONFIG_FILENAME, "w") as file_obj:
            file_obj.write(unicode(json.dumps(configuration.data)))
        logging.debug("write_config - finished")


class ConfigurationFileReader(object):
    """

    Class ConfigurationFileReader provides access to the configuration
    file. It was realised using an matrix of dictionaries (two dimensions).
    Data format: JSON.
    The function read_config() is used to read the configuration in the
    recently explained data structue from a file.

    @author: ssimons

    """

    def __init__(self):
        pass

    @staticmethod
    def read_config():
        """ Reads the the config file and sets the
        appropriate values in the given configuration object.
        @return: data strucutre of the configuration read from file
            (an matrix of dictionaries (two dimensions).
        @raise IOError: If file couldn't be read, an IOError will be raised.
        """
        logging.debug("read_config")

        with open(Configuration.CONFIG_FILENAME) as data_file:
            return json.load(data_file)
