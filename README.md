# MAI_INLP
Repository for the subject "Introduction to Natural Language Processing"

## Instructions on installing Freeling
In order to execute the .py program, it is necessary to have Freeling software installed.
Instructions:

Canviar src/automake_options.am:
if BOOST_OLD
  ADD_FL_DEPS=-lboost_thread$(MT) -lboost_system$(MT)
else
  ADD_FL_DEPS=
endif

Per:

if BOOST_OLD
  ADD_FL_DEPS=-lboost_thread$(MT) -lboost_system$(MT)
else
  ADD_FL_DEPS=-lboost_system$(MT)
endif

1.- Install the dependencies that are specified in the pdf stored in path PATH_TO_FREELING/doc/userman
2.- svn checkout http://devel.cpl.upc.edu/freeling/svn/trunk 
3.- myfreeling
4.- cd myfreeling
5.- autoreconf --install
6.- ./configure
7.- make
8.- sudo make install


