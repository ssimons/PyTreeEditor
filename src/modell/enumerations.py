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

class CustomEnumeration(set):
    """
    CustomEnumeration was added to get a data structure like the Enumeration
    in Java.

    """
    def __getattr__(self, name):
        """ Returns the name of the set of entries.

        """
        if name in self:
            return name
        raise AttributeError

CONFIG_ENUM = CustomEnumeration(["PreSequence", "FirstDelimiter",
                                 "SecondDelimiter", "DataDelimiter",
                                 "highlight_text", "UseDataExpandableInTree",
                                 "UseIgnorePrefix", "IgnorePrefix",
                                 "UseDataPrefix", "StartWithLastFile",
                                 "LastFilename"])


TREE_LEVEL_ENUM = CustomEnumeration(["ROOT", "CHILD",
                                            "CHILD_OF_CHILD", "DATA_EXPANDED"])
