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
import src.modell.tree_operations
from src.modell.logger import logging
from src.modell.enumerations import TREE_LEVEL_ENUM
from src.modell.enumerations import CONFIG_ENUM

class TextExporter(object):
    """
    TextExporter class to save the tree representation to a file.

    """

    def __init__(self, configuration):
        """ Initializes the attributes.
            @param configuration: Configuration object to get the current
                configuration information

        """
        self._conf = configuration

        #use the configuration parameters as variables:
        self.pre_sequence = self._conf.data[str(CONFIG_ENUM.PreSequence)]
        self.first_delimiter = self._conf.data[str(CONFIG_ENUM.FirstDelimiter)]
        self.second_delimiter \
 = self._conf.data[str(CONFIG_ENUM.SecondDelimiter)]

    def export_data_to_line(self, tree_element):
        """Returns the relevant data of the given element.
        The tree element information is used together with all the delimiter
        information from the configuration to produce a str representation
        like it was read from file.
        @param tree_element: the element from which the data should be exported
        @return: str representation of given tree_element.

        """
        export_data_ref = ExportData()
        export_data_ref.complete_line = []
        #Please check comment of get_line_data_elements_to_write_file for
        #order of return value
        export_data_ref.line_data_elems \
 = tree_element.get_line_data_elements_to_write_file(self._conf)
        export_data_ref.extracted_data = export_data_ref.line_data_elems[0]
        remaining_elements_count = len(export_data_ref.line_data_elems[1:])
        export_data_ref.use_line_break_before_line_data = True

        if remaining_elements_count == 3:    # means 2 parents existing
            export_data_ref.complete_line.append(self.pre_sequence)
            #keep in mind that index 0 is the data
            export_data_ref.complete_line.append(\
                export_data_ref.line_data_elems[1])
            export_data_ref.complete_line.append(self.first_delimiter)
            export_data_ref.complete_line.append(\
                export_data_ref.line_data_elems[2])
            export_data_ref.complete_line.append(self.second_delimiter)
            export_data_ref.complete_line.append(\
                export_data_ref.line_data_elems[3])

        if remaining_elements_count == 2:    # means 1 parent existing
            self._export_handle_two_remaining_elements(tree_element,
                                                  export_data_ref)

        if remaining_elements_count == 1:    # means no parents existing
            self._export_handle_one_remaining_element(tree_element,
                                                 export_data_ref)

        # now add blank linebreak and the actual data
        if export_data_ref.use_line_break_before_line_data == True:
            export_data_ref.complete_line.append("\n")
        export_data_ref.complete_line.append(export_data_ref.extracted_data)
        # new replace("\n","<br/>") for displaying highlighted text (html)

        complete_line_string = "".join(export_data_ref.complete_line)
        logging.debug("export_data_to_line called for" + tree_element.label_name
                      + " returned " + complete_line_string.replace("\n", ";"))
        return complete_line_string


    def _export_handle_two_remaining_elements(self,
                                              tree_element,
                                              export_data_reference):
        """ Internal function that uses the given parameter and
        changes the data in it
        @param tree_element: the element from which the data should be exported
        @param export_data_reference: reference to an ExportData object
            that will be altered in this function

        """

        # now we expect that 1 parent exists
        childs_line = []
        childs_line.append(self.pre_sequence)
        #keep in mind that index 0 is the data
        childs_line.append(export_data_reference.line_data_elems[1])
        childs_line.append(self.first_delimiter)
        childs_line.append(export_data_reference.line_data_elems[2])
        #special case:   this element (TREE_LEVEL_ENUM.CHILD)
        #                might have sub-elements
        #                (TREE_LEVEL_ENUM.CHILD_OF_CHILD).
        #                These CHILD_OF_CHILD's are added (respected)
        #                in the next lines (they contain also data).
        #                We don't need the content of "childs_line"
        #                in this case
        use_childs_content = False
        str_child_data = []
        for child_nr in range(tree_element.child_size()):
            if tree_element.children_at(child_nr).tree_level \
                    == TREE_LEVEL_ENUM.CHILD_OF_CHILD:
                use_childs_content = True
                str_child_data.append(self.export_data_to_line(
                    tree_element.children_at(child_nr)))
                export_data_reference.extracted_data = "".join(str_child_data)
                #only add first line (mainIdentifier with
                #presequence if no sub element(child) was collected
                #because the output of a child already contains
                #it (mainIdentifier and its presequence)

        if use_childs_content:
            #don't use a line break because the data element
            #already contain line breaks
            export_data_reference.use_line_break_before_line_data = False
        else:
            export_data_reference.complete_line.append("".join(childs_line))


    def _export_handle_one_remaining_element(self,
                                             tree_element,
                                             export_data_reference):
        """ Internal function that uses the given parameter and
        changes the data in it
        @param tree_element: the element from which the data should be exported
        @param export_data_reference: reference to an ExportData object
            that will be altered in this function

        """

        # now we expect that no parents exists

        #use the sub-elements because they contain the data
        str_child_data_list = []
        str_child_data_list.append(export_data_reference.extracted_data)
        own_data_list_size = len(export_data_reference.extracted_data)
        for child_nr in range(tree_element.child_size()):
            str_child_data_list.append(
                self.export_data_to_line(tree_element.children_at(child_nr)))
        export_data_reference.extracted_data = "".join(str_child_data_list)
        #only add first line (mainIdentifier with presequence
        #if no sub element(child) was collected
        #because the output of a child already contains it
        #(mainIdentifier and its presequence)
        if len(export_data_reference.extracted_data) == own_data_list_size:
            export_data_reference.complete_line.append(self.pre_sequence)
            #keep in mind that index 0 is the data
            export_data_reference.complete_line.append(\
                export_data_reference.line_data_elems[1])
        else:
            export_data_reference.use_line_break_before_line_data = False



    def write_file_from_data(self, tree_instance, filename):
        """ Writes the information of the tree elements to a file.
        The order of the elements from the source file will be respected by
        following the order of the attribute order_of_elements_references.
        Initially this list of order_of_elements_references has to be filtered
        to avoid writing tree elements twice to the file.
        @param tree_instance: Tree object which should
            be written to file
        @param filename: absolute filename of file to save.

        """
        export_elements \
 = list(tree_instance.order_of_elements_references)

        for elem in tree_instance.order_of_elements_references:

            #now ignore all sub-elements of the current one from
            #the execution list(order_of_elements_references)
            #because otherwise entries will appear double or twice
            logging.debug("write_file_from_data pre-filter: " + elem.label_name)
            for child in src.modell.tree_operations.childs_of_element(elem):
                try:
                    if child in export_elements:
                        logging.debug("write_file_from_data children "
                            + "pre-filter: " + child.label_name
                            + "<-- won't be used for export because parent "
                            + "element already there")
                        export_elements.remove(child)
                except ValueError, exc:
                    #child not in list
                    logging.warn("following exception ValueError might "
                                 + "be acceptable because child probably"
                                 + " not in list?")
                    logging.exception(exc)

        try:
            file_obj = open(filename, "w")
            for elem in export_elements:
                logging.debug("write_file_from_data order: " + elem.label_name)
                file_obj.write(self.export_data_to_line(elem))
            file_obj.close()
        except UnicodeDecodeError as exc:
            logging.exception(exc)
            logging.error("Could not open file. Please avoid german "
                          + "umlaut in files and folder under unix")
            return


        #test purpose
        for elem in tree_instance.order_of_elements_references:
            logging.debug("write_file_from_data pre-filter: " + elem.label_name)


class ExportData(object):
    """
    Wrapper class for TextExporter

    """
    def __init__(self):
        self.complete_line = None
        self.line_data_elems = None
        self.extracted_data = None
        self.use_line_break_before_line_data = None
