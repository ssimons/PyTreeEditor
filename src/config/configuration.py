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
class Configuration(object):
    """

    Configuration is represented by an dictionary.
    Values can be accessed using the keys of an enumeration.

    @author: ssimons

    """

    #constant value
    CONFIG_FILENAME = "tree_editor.conf"

    def __init__(self):
        """
        Initializes the attributes with default values.

        """
        self.data = dict(PreSequence='@', FirstDelimiter=' ',
                         SecondDelimiter='', UseDataPrefix=False,
                         DataDelimiter='', UseDataExpandableInTree=False,
                         UseIgnorePrefix=False, IgnorePrefix='',
                         highlight_text=[['#ff0000', 'DUPLICATE:']],
                         StartWithLastFile=False, LastFilename='')
