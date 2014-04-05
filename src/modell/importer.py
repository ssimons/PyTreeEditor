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

import re
import os
import src.modell.tree_operations
from src.modell.logger import logging
from src.modell.enumerations import TREE_LEVEL_ENUM
from src.modell.treestruct.tree_element import TreeElement
from src.modell.enumerations import CONFIG_ENUM
from PyQt4.QtGui import QProgressDialog
from PyQt4.Qt import Qt

class TextImporter(object):
    """
    TextImporter class to realise opening a txt file.
    The interpretation of lines to the own data structure of tree elements
    is realised within the function interpret_line. Remember to call
    inititialize_interpret before using interpret_line!


    """

    #explanation of escapes for attribute "wordIncOtherChar"
    #3B = ;        #2D = -            #2C = ,        #26 = &
    #2E = .        #23 = #            #2B = +        #2F = /
    #2A = *        #28 and 29 ()      #7B = {        #7D = }
    #5F = _

    #represents allowed characters to use in the regular expression
    wordIncOtherChar \
 = r"[a-zA-Z0-9\x3B\x2D\x2C\x2E\x23\x2B\x2A\x28\x29\x2F\x26\x7B\x7D\x5F]"

    DUPLICATE_STR = "DUPLICATE:"

    def __init__(self, configuration):
        """ Initializes the attributes.
            @param configuration: Configuration object to gett the current
                configuration information

        """
        self._conf = configuration
        self.match_re = str()

        #remainder_lines: list of ignored lines
        self.remainder_lines = []
        self._ignore_the_following_datalines = True

        #use the configuration parameters as variables:
        self.pre_sequence = self._conf.data[str(CONFIG_ENUM.PreSequence)]
        self.first_delimiter = self._conf.data[str(CONFIG_ENUM.FirstDelimiter)]
        self.second_delimiter \
 = self._conf.data[str(CONFIG_ENUM.SecondDelimiter)]

        # remembers the tree element which was lastly added to the tree.
        self.last_added_custom_item = None

        self._use_first_delimiter = False
        if self.first_delimiter != "":
            self._use_first_delimiter = True

        self._use_second_delimiter = False
        if self.second_delimiter != "":
            self._use_second_delimiter = True

        self.inititialize_interpret()


    def read_file(self, parent, filename, tree_instance):
        """ Reads text file and calls the interpret_line() function to
        add the file information to the given tree. ImportResult will be
        shown afterwards which lists lines that weren't covered by the
        configuration delimiters.
        The model / view will be notified after the file reading to rebuild
        the view. It isn't necessary to do every time in the for-loop.
        @param parent: Use this object for QProgressDialog (modal window)
        @param tree_instance: Tree object where the
            new tree elements should be added to.
        @return: remainder_lines - list of not imported lines.
        """

        self.inititialize_interpret()

        try:


            max_lines = self._count_lines(filename)

            progress_bar = QProgressDialog("Importing lines...", "Abort",
               0, max_lines, parent)
            progress_bar.setWindowModality(Qt.WindowModal)

            file_obj = open(filename, "r")
            for line_no, zeile in enumerate(file_obj):
                logging.debug("read_file:" + zeile)
                self.interpret_line(zeile, tree_instance)

                progress_bar.setValue(line_no)
                if progress_bar.wasCanceled():
                    break
            progress_bar.setValue(max_lines)
            file_obj.close()
        except re.error, exc:
            logging.exception(exc)
            file_obj.close()
        except UnicodeDecodeError as exc:
            logging.exception(exc)
            logging.error("Could not open file. Please avoid german umlaut"
                          + "in files and folder under unix")
            file_obj.close()
            return




        try:
            tree_instance.set_file_name(os.path.basename(str(filename)))
        except AttributeError, exc:
            logging.exception(exc)

        tree_instance.fire_data_changed()
        return self.remainder_lines

    def _count_lines(self, filename):
        try:
            return sum(1 for l in open(filename))
        except UnicodeDecodeError as exc:
            logging.exception(exc)
            logging.error("Could not open file. Please avoid german "
                          + "umlaut in files and folder under unix")
            return


    def inititialize_interpret(self):
        """Initializes all the attributes that are used in the
        interpret_line() function. Therefore it should be
        called before every calling the interpret_line().

        """
        self._ignore_the_following_datalines = False
        self.last_added_custom_item = None
        self.remainder_lines = []

        self.match_re = str()
        self.match_re += "" + re.escape(self.pre_sequence) \
            + "{1}" + self.wordIncOtherChar + "+(" \
            + re.escape(self.first_delimiter) + "){0,1}" \
            + self.wordIncOtherChar + "+(" \
            + re.escape(self.second_delimiter) + "){0,1}" \
            + self.wordIncOtherChar + "*"

    def interpret_line(self, line, tree_instance):
        """
        Interpreting a line by using a regular expression to check which lines
        match the expression. These are the lines for the tree elements. All
        the other lines are used as data lines or are ignored (depending on
        the configuration).
        Please ensure that the inititialize_interpret() is called
        before this function is used.
        Also please keep in mind that the ignored lines are added to the
        attribute self.remainder_lines  (type list). They might be used
        afterwards to print them.
        @param line: line of type str to interpret
        @param tree_instance: Tree object where the
            new tree elements should be added to.

        """
        logging.debug("interpret_line. line (size:"
                      + str(len(line)) + "):" + line)
        #initially check whether the line could be ignored
        #(because of the configuration)
        if self._conf.data[str(CONFIG_ENUM.UseIgnorePrefix)] == True \
                and line.startswith(self._conf.data[
                    str(CONFIG_ENUM.IgnorePrefix)]):

            logging.debug("Line ignored (config value: %s ):%s",
                          self._conf.data[str(CONFIG_ENUM.IgnorePrefix)], line)
            return

        if len(line.strip()) == 0:
            logging.debug("Line is empty (size 0) -> ignore")
            return

        #line example = "@identifier Foo1"
        logging.debug("interpret_line. match_re:" + self.match_re)

        match_obj = re.match(self.match_re, line)
        if match_obj is not None:
            #regular expression matched current line: identifier line
            self._interpret_identifier_line(line, tree_instance)
        else:
            #regular expression *did not* match current line: *no* identifier
            #e.g. a data line
            self._interpret_none_identifier_line(line, tree_instance)


    def _interpret_none_identifier_line(self, line, tree_instance):
        """ Handles  the *non* identifier lines(e.g. data line or something to
        ignore.
        @param line: line of type str to interpret
        @param tree_instance: Tree object where the
            new tree elements should be added to.

        """
        if self.last_added_custom_item  is None:
            logging.debug("Put Line to remainder because"
                + "last_added_custom_item  is None"
                + "line:" + line)
            self._add_element_to_remainder_list(line, True)
        else:

            if self._check_for_data_line(line):
                self._handle_data_line(line, tree_instance)
            else:
                # no data line - just put it to the remainder list
                logging.debug("Put Line to remainder because"
                    + "_check_for_data_line returned False."
                    + "Lastly added exists. line:" + line)
                self._add_element_to_remainder_list(line, True)


    def _check_for_data_line(self, line):
        """Conditions to decide whether it’s a data line became longer -
        therefore I moved it to this function.

        @param line: line of type str to interpret
        @return: True for data lines - False to ignore
        """

        #Now decide whether it's a data line or not
        #using the flag _ignore_the_following_datalines helps us
        #to ensure that after a main line (with prefix and
        #stuff like that) which wasn't respected (->ignored)
        #the following data lines will also be ignored

        use_data_prefix = self._conf.data[str(CONFIG_ENUM.UseDataPrefix)]
        data_prefix = self._conf.data[str(CONFIG_ENUM.DataDelimiter)]

        if self._ignore_the_following_datalines == False \
                and ((use_data_prefix == True and line.startswith(data_prefix))\
                    or use_data_prefix == False):

            return True
        else:
            # no data line
            return False

    def _add_element_to_remainder_list(self, line, is_data_tree_element):
        """ The remainder list is an object attribute with all the lines that
        were skipped/ignored by the importer
        @param line: line of type str to interpret (e.g. read line from file)
        @param is_data_tree_element: we habe to differ between data tree
            elements and non data tree elements.
        """
        if len(line.strip()) > 0:
            self.remainder_lines.append(line)
            if not is_data_tree_element:
                self._ignore_the_following_datalines = True

            logging.debug("IGNORING the following line because no "
                + "pattern applyable. (attr ignore_the_following_"
                + "datalines="
                + str(self._ignore_the_following_datalines) + "):"
                + line)

    def _handle_data_line(self, line, tree_instance):
        """ A data line might be determined by the special character(s)
        that were set in the configuration.
        @param line: line of type str to interpret
        @param tree_instance: Tree object where the
            new tree elements should be added to.

        """
        logging.debug("_handle_data_line:%s", line)
        #Should the element be added as just as data text - or as tree element?
        if self._conf.data[str(CONFIG_ENUM.UseDataExpandableInTree)] is False:

            #add just the string data to the element
            self.last_added_custom_item.add_line_data(line)
        else:
            item_data, was_datad_already_existing \
 = self._handle_import_element((line[1:]).replace("\n", ""),
                                              TREE_LEVEL_ENUM.DATA_EXPANDED,
                                              tree_instance,
                                              self.last_added_custom_item)
            if not was_datad_already_existing:
                logging.debug("adding/using data element "
                              + item_data.label_name + " alreadyExists:"
                              + str(was_datad_already_existing))
            else:
                logging.debug("data element already there. put line to the "
                              "remainder: %s", line)
                self._add_element_to_remainder_list(self.DUPLICATE_STR + line,
                                                    True)

    def _interpret_identifier_line(self, line, tree_instance):
        """Handle the indentifier line which will be used as tree elements.
        @param line: line of type str to interpret
        @param tree_instance: Tree object where the
            new tree elements should be added to.

        """
        self._ignore_the_following_datalines = False
        added_tree_level = []
        extracted_line = line.replace("\n", "")

        identifiers = self._extract_identifiers_from_line(extracted_line)

        #note for rootElement that the parent element is the
        # treeeWidgetInstance itself - the child element uses their parent
        item_root_element, was_root_already_existing = \
            self._handle_import_element(identifiers.main1,
                                       TREE_LEVEL_ENUM.ROOT,
                                       tree_instance,
                                       tree_instance)
        logging.debug("adding/using tree element "
                      + item_root_element.label_name
                      + " alreadyExists:" + str(was_root_already_existing))
        added_tree_level.append(TREE_LEVEL_ENUM.ROOT)


        was_child_already_existing = False
        if identifiers.main2 != "":
            item_child_element, was_child_already_existing = \
                self._handle_import_element(identifiers.main2,
                                            TREE_LEVEL_ENUM.CHILD,
                                            tree_instance,
                                            item_root_element)
            tree_instance.order_of_elements_references.append(
                item_child_element)    #put it ordered to the list
            logging.debug("adding to order_of_elements_references :"
                          + identifiers.main2)
            self.last_added_custom_item = item_child_element
            logging.debug("adding/using tree element "
                          + item_child_element.label_name
                          + " alreadyExists:"
                          + str(was_child_already_existing))
            added_tree_level.append(TREE_LEVEL_ENUM.CHILD)
        else:
            #special case: only item1Root element exists without sub-element.
            # put it in the orderedList  (because no child element will
            # be added). this list ensures the given order (at the time
            # it was loaded from the file)
            tree_instance.order_of_elements_references.append(
                item_root_element)
            logging.debug("adding to order_of_elements_references :"
                          + identifiers.main1)
            self.last_added_custom_item = item_root_element

        child_of_child_already_existing = False
        if identifiers.main3 != "":
            item_child_of_child_element, child_of_child_already_existing  \
 = self._handle_import_element(identifiers.main3,
                                                TREE_LEVEL_ENUM.CHILD_OF_CHILD,
                                                tree_instance,
                                                item_child_element)
            tree_instance.order_of_elements_references.append(
                item_child_of_child_element)    #put it ordered to the list
            logging.debug("adding to order_of_elements_references :"
                          + identifiers.main3)
            self.last_added_custom_item = item_child_of_child_element
            logging.debug("adding/using tree element "
                          + item_child_of_child_element.label_name
                          + " alreadyExists:"
                          + str(child_of_child_already_existing))
            added_tree_level.append(TREE_LEVEL_ENUM.CHILD_OF_CHILD)

        self._put_duplicates_to_remainder(line, added_tree_level,
            was_root_already_existing,
            was_child_already_existing, child_of_child_already_existing)


    def _extract_identifiers_from_line(self, line):
        """ Extracts and returns the identifiers (main1, main2, main3)
        according to the delimiters of the configuration.
        @param line: line of type str to interpret
        @return: Identifiers object as wrapper
        """

        #special case: no first_delimiter set ("") -> just return full line
        #              as main1
        if not self._use_first_delimiter:
            line_without_presequence = line[len(self.pre_sequence):]
            logging.debug("interpret_line. extracted main1: %s",
                          line_without_presequence)
            return Identifiers(line_without_presequence, "", "")

        #line example = "@Identifier Foo1"
        main1 = line[len(self.pre_sequence) :
                     line.index(self.first_delimiter,
                                (len(self.pre_sequence) + 1))]
        logging.debug("interpret_line. extracted main1:" + main1)
        index_after_main1_old = len(self.pre_sequence) \
            + len(main1) + len(self.first_delimiter)
        index_after_main1 \
 = line.index(self.first_delimiter) + len(self.first_delimiter)
        logging.debug("index_after_main1_old="
                     + str(index_after_main1_old)
                     + "  index_after_main1=" + str(index_after_main1))
        main3 = ""
        try:
            index_second_delimiter = line.index(self.second_delimiter,
                                                (index_after_main1 + 1))
        except ValueError:
            index_second_delimiter = -1
            logging.debug("index_second_delimiter caused ValueError while using"
                         + " second_delimiter="
                         + str(self.second_delimiter)
                         + " indexAftermain+1="
                         + str(index_after_main1 + 1))
        logging.debug("using main3 "
                     + str(self._use_second_delimiter)
                     + " pos: " + str(index_second_delimiter))

        if self._use_second_delimiter and index_second_delimiter > -1:
            len_second_delimiter = len(self.second_delimiter)
            main3 = line[(index_second_delimiter + len_second_delimiter):]

            # special case: typically we would just call the following
            #     main2 = line[index_after_main1:
            #                            index_second_delimiter]
            # but I encountered the case that main3 (after the
            # second_delimiter) was empty (""). In this case it might be good
            # to use the rest of the line as main2 element instead of
            # just using the few charcaters till the second delimiter
            # example: aa @ bb  with @ as second delimiter won't work.
            # the spaces are the problem.
            #          solution delimiter =" @ ". But the gui would
            #          only display "aa " as element - which may
            #          confuse some people because the line is longer
            if main3 != "":
                main2 = line[index_after_main1:index_second_delimiter]
            else:
                main2 = line[index_after_main1:]
        else:
            main2 = line[index_after_main1:]

        logging.debug("interpret_line. extracted main2:" + main2)
        logging.debug("interpret_line. extracted main3:" + main3)

        return Identifiers(main1, main2, main3)

    def _handle_import_element(self, label_name_of_element, tree_level,
                              tree_instance, parent_of_tree_element):
        """ Internal function of interpret_line() to check whether the
        element does already exist. When it doesn't exist, it should be added.
        Returns this information as list/tupel (check @return).
        @param label_name_of_element: label name of tree element as str object
        @param tree_level: TREE_LEVEL_ENUM object as level
        @param tree_instance: Tree object where the
            new tree elements should be added to.
        @param parent_of_tree_element: Parent element of the tree element that
        should be created - expects type of Tree or TreeElement
        @param line: line of type str to interpret
        @return: a tupel of the item_element and a bool value whether the
            item does already exist:  [item_element,alreadyExisting]

        """

        # try to find existing mainIdentifier (beginning after the
        # presequence for TREE_LEVEL_ENUM.DATA_EXPANDED just
        # search in the data elements of the current element
        search_in_tree_elements = tree_instance.get_children()
        if tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED:
            search_in_tree_elements \
 = src.modell.tree_operations.childs_of_element(parent_of_tree_element)
        item_elem_existing \
 = src.modell.tree_operations.find_element_by_level(label_name_of_element,
                                 tree_level,
                                 search_in_tree_elements)

        if item_elem_existing is None:
            item_elem = TreeElement(label_name_of_element,
                                    tree_level,
                                    parent_of_tree_element)

            parent_of_tree_element.add_children_without_modelnotify(item_elem)

        else:
            item_elem = item_elem_existing

        return [item_elem, (item_elem_existing is not None)]


    def _put_duplicates_to_remainder(self, line, added_tree_level,
            was_root_already_existing, was_child_already_existing,
            child_of_child_already_existing):
        """Puts tree elements to the remainder_list if they are duplicate *and*
        aren't needed for sub elements. The following example points out the
        last case.
        Example:
        "@identifier sub_ident" where "identifier" is the root and "sub_ident"
        the child. Let's assume that "@identifier another_sub_ident" was already
        processed. Therefore identifier is still present in the tree and
        "was_root_already_existing" will be true. But it is needed for the
        second identifier (the child) "sub_ident". In this case the root won't
        be put to the remainder.
        """

        if TREE_LEVEL_ENUM.CHILD_OF_CHILD in added_tree_level:
            if child_of_child_already_existing:
                logging.debug("element already there. put line to the "
                              "remainder: %s", line)
                self._add_element_to_remainder_list(self.DUPLICATE_STR + line,
                                                    False)
        elif TREE_LEVEL_ENUM.CHILD in added_tree_level:
            if was_child_already_existing:
                logging.debug("element already there. put line to the "
                              "remainder: %s", line)
                self._add_element_to_remainder_list(self.DUPLICATE_STR + line,
                                                    False)
        elif TREE_LEVEL_ENUM.ROOT in added_tree_level:
            if was_root_already_existing:
                logging.debug("element already there. put line to the "
                              "remainder: %s", line)
                self._add_element_to_remainder_list(self.DUPLICATE_STR + line,
                                                    False)

class Identifiers(object):
    """
    Wrapper class for TextImporter

    """
    def __init__(self, main1, main2, main3):
        self.main1 = main1
        self.main2 = main2
        self.main3 = main3

    def __eq__(self, second):
        """ __eq__ fucntion with class specific comparison.

        """
        return  self.main1 == second.main1 \
            and self.main2 == second.main2 \
            and self.main3 == second.main3
