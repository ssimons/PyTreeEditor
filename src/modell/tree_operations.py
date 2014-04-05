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

import src.modell.importer
import src.modell.exporter
import src.gui.gui_helper
from src.modell.logger import logging
from src.modell.enumerations import TREE_LEVEL_ENUM
from src.modell.treestruct.tree_exceptions import NoProperTreeElementException, \
    NotEnoughTreeElementsCheckedException, TreeElementsNotSameLevelException

def find_checked_elements(tree_root_elements,
                         no_childelements_for_higher_elements,
                         one_data_element_per_level):
    """ Returns a list of selected elements of the given tree_root_elements,
    (!) and their children, respecting the restrictions of the other
    parameters. Selected means that the checkboxes of the tree element is
    checked.
    @param tree_root_elements: a list of tree elements
    @param no_childelements_for_higher_elements: if higher level tree
        elements are checked, assume that all kind elements
        are included and don't need to be added to the checkedList
    @param onlyReturnOneElementPerLevel - if another element is at
        the same level selected, only the first should
        be marked as selected. E.g. for example for printing
        purposes that the whole tree shouldn't be printed
        multiple times. Typically this option is used for data
        element entries.
    @return: a list of selected elements.
    """
    checked_elements = []
    for i in tree_root_elements:
        if i.check_state_bool() == True:
            checked_elements.append(i)
            if no_childelements_for_higher_elements == True:
                continue
        children = childs_of_element(i)
        childs_selected = find_checked_elements(
            children, no_childelements_for_higher_elements,
            one_data_element_per_level)
        at_least_one_data_element_selected = False
        for child_sel in childs_selected:

            if  one_data_element_per_level == True \
                and at_least_one_data_element_selected == True \
                and child_sel.tree_level \
                    == TREE_LEVEL_ENUM.DATA_EXPANDED:
                break
            checked_elements.append(child_sel)
            at_least_one_data_element_selected = True

    return checked_elements

def find_element_by_level(label_name, tree_level, tree_collection):
    """Searches the first occurence of the given labe_name at the given
    tree_level of the given tree_collection. (!) Child results will be
    included to the output.
    @param label_name: str object - the name of the tree element.
    @param tree_level: TREE_LEVEL_ENUM object that indicates the
        level of the tree element.
    @param tree_collection: a list of tree elements

    """
    for i in tree_collection:
        if tree_level == i.tree_level \
                and label_name.upper() == i.label_name.upper():
            return i
        children = childs_of_element(i)
        child_result = find_element_by_level(label_name,
                                                  tree_level,
                                                  children)
        if child_result is not None:
            return child_result


def childs_of_element(element):
    """ Returns all children of the current Tree / TreeElement as a list

    """
    children = []
    for sub_index in range(element.child_size()):
        children.append(element.children_at(sub_index))
    return children

def data_down_move(tree_instance):
    """ Moves data of selected elements one line / row below. The last
    element won't be moved. Selected means that the checkboxes of the tree
    element is checked.
    @param tree_instance: Tree object that should be used.
    @return: result list of successfull operations
    """
    result_successfull = []
    for elem in list(reversed(
                find_checked_elements(tree_instance.get_root_elements(),
                                      False, False))):
        if elem.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED:
            logging.debug("data_down_move:" + elem.label_name)
            current_element_label = elem.label_name
            parent_elem = elem.parent()
            current_index = parent_elem.get_children().index(elem)
            logging.debug("data_down_move - index:" + str(current_index)
                          + " size: " + str(parent_elem.child_size()))
            if (current_index + 1) < parent_elem.child_size():

                #swap_elements
                parents_children = parent_elem.get_children()
                parents_children[current_index + 1], \
                        parents_children[current_index] \
 = parents_children[current_index], \
                        parents_children[current_index + 1]

                logging.debug("data_down_move finished - new index:" +
                               str(parent_elem.get_children().index(elem)))
                result_successfull.append(current_element_label)

    #notify listener to update GUI
    tree_instance.fire_data_changed()
    return result_successfull

def data_up_move(tree_instance):
    """ Moves data of selected elements one line / row above. The first
    element won't be moved. Selected means that the checkboxes of the
    tree element is checked.
    @param tree_instance: Tree object that should be used.
    @return: result list of successfull operations
    """
    result_successfull = []
    for elem in find_checked_elements(tree_instance.get_root_elements(),
                                      False, False):
        if elem.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED:
            logging.debug("data_up_move:" + elem.label_name)
            current_element_label = elem.label_name
            parent_elem = elem.parent()
            current_index = parent_elem.get_children().index(elem)
            logging.debug("data_up_move - old index" + str(current_index))
            if (current_index - 1) >= 0:

                #swap_elements
                parents_children = parent_elem.get_children()
                parents_children[current_index - 1], \
                        parents_children[current_index] \
 = parents_children[current_index], \
                    parents_children[current_index - 1]

                logging.debug("data_up_move finished - new index:" +
                               str(parent_elem.get_children().index(elem)))
                result_successfull.append(current_element_label)

    #notify listener to update GUI
    tree_instance.fire_data_changed()
    return result_successfull


def exchange_elements(tree_instance):
    """ Exchanges the two (!) selected tree elements.
    @param tree_instance: Tree object that should be used.
    @raise NotEnoughTreeElementsCheckedException: If != 2 tree elemts are
        checked this exception will be raised
    @raise NoProperTreeElementException: If tree element couldn't be
        determined (e.g. not proper level) this exception is raised
    """

    selected_items = find_checked_elements(tree_instance.get_root_elements(),
                                          False, False)
    if len(selected_items) != 2:
        raise NotEnoughTreeElementsCheckedException(
            "You have to select 2 elements")

    first_element = selected_items[0]
    second_element = selected_items[1]

    if ((first_element.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED
               and second_element.tree_level != TREE_LEVEL_ENUM.DATA_EXPANDED)
            or (first_element.tree_level != TREE_LEVEL_ENUM.DATA_EXPANDED
               and second_element.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED)):
        raise NoProperTreeElementException("One data tree element and one "
            + "normal tree element checked. Please only select 2 elements of "
            + "the same type (either data tree element or normal tree "
            + "elements)")


    index_0_found = False
    index_1_found = False
    try:
        index0 = tree_instance.order_of_elements_references.index(
            selected_items[0])
        index_0_found = True
    except ValueError:
        pass

    try:
        index1 = tree_instance.order_of_elements_references.index(
            selected_items[1])
        index_1_found = True
    except ValueError:
        pass

    if index_0_found and index_1_found:
        logging.debug("Exchange also the order_of_elements_references")
        temp_elem = selected_items[0]
        tree_instance.order_of_elements_references[index0] \
 = tree_instance.order_of_elements_references[index1]
        tree_instance.order_of_elements_references[index1] = temp_elem

    _exchange_data_elements(selected_items)

    #notify listener to update GUI
    tree_instance.fire_data_changed()

    #exception for information purpose
    if first_element.tree_level != second_element.tree_level:
        raise TreeElementsNotSameLevelException("The select tree elements "                        
            + "doesn't have the same level (e.g. one is root, one is child of "
            +" child). This is tolerated, but be cautious when saving the file."
            +"Because it will corrupt your output file.")

def _exchange_data_elements(two_checked_data_tree_elements):
    first_element = two_checked_data_tree_elements[0]
    second_element = two_checked_data_tree_elements[1]

    parent_of_first = first_element.parent()
    parent_of_second = second_element.parent()

    if parent_of_first is not None and parent_of_second is not None:

        first_index_of_parent = \
            parent_of_first.get_children().index(first_element)
        second_index_of_parent = \
            parent_of_second.get_children().index(second_element)

        if parent_of_first == parent_of_second:
            #swap_elements
            parents_children = parent_of_first.get_children()
            parents_children[first_index_of_parent], \
                    parents_children[second_index_of_parent] \
 = parents_children[second_index_of_parent], \
                parents_children[first_index_of_parent]
        else:
            if first_element.tree_level == TREE_LEVEL_ENUM.DATA_EXPANDED:
                del parent_of_first.get_children()[first_index_of_parent]
                del parent_of_second.get_children()[second_index_of_parent]
                first_element.parent_element = parent_of_second
                second_element.parent_element = parent_of_first
                parent_of_first.get_children().insert(first_index_of_parent,
                                                      second_element)
                parent_of_second.get_children().insert(second_index_of_parent,
                                                       first_element)
            else:
                parent_of_first.remove_children_without_modelnotify(
                    first_element)
                parent_of_second.remove_children_without_modelnotify(
                    second_element)
                first_element.parent_element = parent_of_second
                second_element.parent_element = parent_of_first
                firsts_level = first_element.tree_level
                first_element.tree_level = second_element.tree_level
                second_element.tree_level = firsts_level
                parent_of_first.add_children_at_without_modelnotify(
                    first_index_of_parent, second_element)
                parent_of_second.add_children_at_without_modelnotify(
                    second_index_of_parent, first_element)



def tree_element_change_label(tree_instance, new_label):
    """ replaces the label_name of the selected elements. The QInputDialog
    is used to type in the new value.Selected means that the checkboxes of
    the tree element is checked.
    Hint: Calling the function when selecting tree item could be helpful
        to update the editor
    @param tree_instance: Tree object that should be used.
    @param new_label: the label/name to change / replace
    """

    result_successfull = []
    for elem in find_checked_elements(tree_instance.get_root_elements(),
                                      False, False):
        current_element_label = elem.label_name
        elem.change_label(unicode(new_label))
        result_successfull.append(current_element_label)


    #notify listener to update GUI
    tree_instance.fire_data_changed()
    return result_successfull



def copy_elements_to_other_tree(tree_instance_from,
                                tree_instance_to,
                                config):
    """ Internal function in order to determine selected elements of the
    tree_instance_from and copy them  to the tree_instance_to. The text
    representation of the source is used in order to use the import
    routine (cf. TextImporter class).Selected means that the checkboxes of
    the tree element is checked.
    @return: remainder_list list of ignored text lines
    """
    checked_elements = find_checked_elements(
        tree_instance_from.get_root_elements(), True, True)
    _importer = src.modell.importer.TextImporter(config)
    _exporter = src.modell.exporter.TextExporter(config)
    for i in checked_elements:
        logging.debug("Copy to main tree: " + i.label_name)
        #handle incoming treeElement (string text) as it is handled
        #when reading from file:
        element_to_add_as_string = _exporter.export_data_to_line(i)
        logging.debug("_copy_elements_to_other_tree. "
                      + "element_to_add_as_string:"
                      + element_to_add_as_string)
        for zeile in element_to_add_as_string.split("\n"):
            logging.debug("_copy_elements_to_other_tree. addNewEntry:"
                          + zeile)
            _importer.interpret_line(zeile, tree_instance_to)

    tree_instance_to.fire_data_changed()
    return _importer.remainder_lines

def remove_element_is_from_tree(tree_instance):
    """ Removes checked elements.
    @param tree_instance: Tree object that should be used.
    @return: a list of failed elements to delete.
    """
    checked_elements = find_checked_elements(
        tree_instance.get_root_elements(), False, False)

    failed_elements = []

    for checked_element in checked_elements:
        logging.info("Remove from main tree: " + checked_element.label_name)

        try:

            delete_childs_in_order_of_elems(tree_instance, checked_element)

            if checked_element in tree_instance.order_of_elements_references:
                tree_instance.order_of_elements_references. \
                    remove(checked_element)
            checked_element.remove_this_element()
        except ValueError, exc:
            logging.exception(exc)
            failed_elements.append(checked_element.label_name)

    tree_instance.fire_data_changed()
    return failed_elements


def delete_childs_in_order_of_elems(tree_instance, element):
    """ Internal function used by remove_element_is_from_tree to consider
    the children of the current elemet. Therefore the children
    have to be deleted in the order_of_elements_references list.

    """
    if element.tree_level != TREE_LEVEL_ENUM.DATA_EXPANDED:

        if element in tree_instance.order_of_elements_references:
            logging.debug("delete_childs_in_order_of_elems: element from "
                          + "order_of_elements_references deleted: "
                          + element.label_name)
            tree_instance.order_of_elements_references.remove(
                element)

        #children:
        for elem in childs_of_element(element):
            delete_childs_in_order_of_elems(tree_instance,
                                                    elem)



def show_data_text_of_checked_tree_elements(tree_root_elements,
                                            configuration,
                                            text_output_instance,
                                            text_output_string):
    """ Action when an tree-element is checked.
    Will run throught the check elements to display its data in
    the given text output field.
    @tree_root_elements: the root elements of the current tree.
    @configuration: object of type Configuration
    @param text_output_instance: QTextEdit object.
    @param text_output_string: QString object

    """
    text_output_string.clear()
    checked_elements = find_checked_elements(tree_root_elements,
                                                 True, True)
    exporter = src.modell.exporter.TextExporter(configuration)
    for i in checked_elements:
        logging.info("CHECKED_ELEMENTS=" + i.label_name)
        text_output_string.append(
            src.gui.gui_helper.format_colored_text(configuration,
                                       exporter.export_data_to_line(i)))

    text_output_instance.setHtml(text_output_string)



def data_search_and_replace(parent, tree_instance):
    """
    TODO: immplement function and enable data_search_and_replace_button
    in main_gui
    """
    pass



def print_tree(tree_inst):
    """ Prints the given Tree object recursively.
    """
    for i in tree_inst.get_children():
        logging.debug("    %s", i)
        if i.has_children():
            print_tree(i)
