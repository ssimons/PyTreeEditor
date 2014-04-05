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


@author: ssimons

"""

class ChildrenAlreadyExistsException(Exception):
    def __init__(self, message):
        super(ChildrenAlreadyExistsException, self).__init__(message)

class IndexOutOfBoundsException(Exception):
    def __init__(self, message):
        super(IndexOutOfBoundsException, self).__init__(message)

class ChildrenDoesntExistsException(Exception):
    def __init__(self, message):
        super(ChildrenDoesntExistsException, self).__init__(message)

class NotEnoughTreeElementsCheckedException(Exception):
    def __init__(self, message):
        super(NotEnoughTreeElementsCheckedException, self).__init__(message)

class NoProperTreeElementException(Exception):
    def __init__(self, message):
        super(NoProperTreeElementException, self).__init__(message)

class TreeElementsNotSameLevelException(Exception):
    def __init__(self, message):
        super(TreeElementsNotSameLevelException, self).__init__(message)
