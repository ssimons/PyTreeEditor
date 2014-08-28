PyTreeEditor
===========

PyTreeEditor facilitates the work with large text files (e.g. configuration 
files). 

It finds identifier lines according to the given configuration (prefix, 
first delimiter, etc.) and uses them as „tree children“. 
These indentifier lines and its data are comparable to the heading and its 
paragraphs of an article. The program enables you to navigate fast and work 
easily with the data of the identifier.

<img src="http://www.s-simons.de/img/PyTreeEditor_presentation.png">

### Features:

* **delimiters** for the identifier lines are **configurable**
* easily **navigate** even through **large files**
* **branches** can be **selected** to display their **text representation**
* tree elements can be **edited, exchanged** and **much more**
* open a **second file/tree** to compare or **copy tree elements** to another tree

It is written in Python 2.7 and PyQt4.

The program was inpired by a friend who does computational structural analysis 
with their custom software. He will use the program for their input files.
 
I have realized the delimiters to be configurable so that they can be used for 
a wide range of text formats. Therefore it should be usable with programs like 
[LS-Dyna] (http://de.wikipedia.org/wiki/LS-DYNA), [LaTeX] (http://de.wikipedia.org/wiki/LaTeX) and many others.

In order to learn Python and Qt/PyQt, I have developed this tool.

Feel free to give me feedback. For this, please send me an e-mail: 
ghprojects@s-simons.de

[**Help page**](http://www.s-simons.de/tree_editor_help.html)

[**Project site**] (http://www.s-simons.de/tree_editor.html)

**Download** 
- [Version 0.9.0 for Windows (8.9 MB)] (http://www.s-simons.de/freeware/PyTreeEditor.zip)
- [Version 0.9.0 for Linux binary (40.1 MB - PyQt included)] (http://www.s-simons.de/freeware/tree_editor.tar.gz)
- Alternatively download zipped source from github and start "tree_editor.py".



