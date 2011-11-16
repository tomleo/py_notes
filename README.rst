=================
Programming Notes
=================

A Note Taking Method for programmers

********
Overview
********

The idea behind this project is to take a simple note taking format and render
a clean html representation of that note with features like syntax highlighting.

Basic Syntax
------------

::

   h1: title of topic goes here
   h2: sub topic title goes here
   p: regular text goes in paragraph tags
   h2: headings and paragraph
   tags can span
   multiple columns
   ps: this tag is used to display mulitple elements seperated
       by newlines. each element should be different but related.
   code<lang>:
       int main(){
           cout<"Hello!"
       }
   endcode

Syntax explained
----------------

h1-h9
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Headings h1-h6 have the same function as <h1>-<h6> headings in html.
Everything below an h1 tag is interpreted as a child of the h1 tag.
With the parent-child relation-ship between headings, subheadings,
paragraphs, and code; organizing documentation and inserting
information into the right place of a large document is very simple.

p
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The p or paragraph tag is simply for paragraphs of text.
I have not decided if code snipets should be inside of paragraphs,
or simply a relation-ship is defined based on their parent heading.

ps (name will probably change)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The idea behind the ps tag is to allow related definitions
to be grouped togeather in one tag, and seperated via a newline.

Example
"""""""

::

   ps:
   find /etc -name '*conf'
   find . -not -name '*.java' -maxdepth 4
   ;

The above example shows diffrent actions you can take with the linux find
comand line program.

code<lang>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The biggest reason for this project is because evernote, google docs, notepad,
ect. does not support syntax highlighting, and text editors that do support
syntax highlighting are for full source code not text snippets.

reStructedText is awesome but for simple notetaking I belive it to be
overkill.

Example
"""""""

::

   code<c++>:
   int main(){
      cout <<"This is C++ code";
   }

code snippets end with "endcode" instead of ";" so that they don't mess with ";" within code snippets.

comments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

//# denotes a special comment that is rendered out of any block of text/code
and placed into a <div>. The idea is to make comments look like they do
in Microsoft Word or Google Docs.

In other wordrs the //# will highlight a line and add a side commenet instead of being a normal comment.

Example
"""""""

::

   ps:
   find . -type f   	//# find files
   find . -size +100M	//# find with size more than 100MB
   ;

************************************
Ideas of features and Implementation
************************************

Feature List
------------

   * Autogenerate a table of contents
   * Create standards complient HTML5 markup
   * Syntax highlighting via pygments
   * Documents style defined with CSS 
   * Some type of templating support
   * Support for restructed output (instead of HTML)
   * Integrate notes with google docs for cloud backup and note taking
   * Integrate with SVN or Git for history of changes (this will allow colaberation and revision control because all notes are in plain text)
   * Plug-ins for wordpress and blogger so that notes can be blog posts
   * Render notes into json format
   * Render notes into yaml format
   * Themes designed about pygments supported color schemes


Object-Oriented Note Taking structure
-------------------------------------

Tags are organized in a hierarchy:
folder_name - file_name - h1...h9 - p,ps,code

This will allow elements to be dasy chained togeather like css selectors.

Internally each chuch of notes will be broken up in this hierarchy allowing
features like adding to notes from the command line.

Example
^^^^^^^

'cs_notes'.'java.txt'.'class sctructure'.'to string'.append("Defines what will be displayed when printing an object for system.out.print(ln)")

'cs_notes'.'python.txt'.'Django'.edit()

The idea of append is strait forward, add text to a specific section within the notes you are taking.

The second example shows the .edit() function. The idea behind .edit() is to display only the Django section of documentation so that if
you did something like vim 'python.txt'.'Django'.edit() then you only see text for this section of the notes creating a smaller editor buffer. I think this would work well for really large topics.

The GUI
-----------------------

The gui has not yet be written however the idea will be a simple WYSIWYG
application that allows easy note taking without knowing any the markup, and you
see exactly how things will be formated in HTML. Also unlike most WYSIWYG
applications the output will be beautiful standards complient HTML5 code.

The gui could also be an application similar to blogger, where many people can
colaberate on documentation at the same time.

****************************************
WAY MORE IDEAS ON IMPLEMENTATION TO COME
****************************************

Stay tuned :)