Development
===========

.. toctree::
   :maxdepth: 4

	      
Introduction
------------

As you have probably realised by now, EntroPass has been written in Python3. It has been developed, using a virtual environment to keep the development system from getting cluttered and to keep dependency management relatively easy. The dependencies are stored in a text file called "requirements.txt". The project has been developed in a Object Oriented style and has Numpy style Sphinx comments embedded in the code for this documentation and to allow developers to easily identify the purpose of the bits of code. The code was written in a text editor (Emacs, for those interested), and should remain possible to develop on outside of IDE's.

Guidelines
----------

.. attribute:: Python version

   Python3 is used and the project is not compatible with Python2. The exact version at the time of writing is 3.8.6

.. attribute:: Indentation

   The indentation is set to the Emacs Python default, which is 4 spaces.

.. attribute:: Dependencies

   The dependencies are stored in "requirements.txt" in the root directory of the repository. These can be installed in the virtual environment using the following command:

   .. code-block:: bash

      pip install -r requirements.txt

   Outside of the virtual environment, it is possible to install all dependencies in a similar manner, using the following command:

   .. code-block:: bash

      python3 -m pip install -r requirements.txt

   If you installed new dependencies using pip, make sure to update the requirements file:

   .. code-block:: bash

      pip freeze > requirements.txt

.. attribute:: Virtual Environment

   The virtual environment is not included in the repository, since it is system specific. To create a virtual environment, navigate to the root directory of the repository and use the following command:

   .. code-block:: bash

      python3 -m venv venv

   After this, activate the virtual environment:

   .. code-block:: bash

      source venv/bin/activate

   Next, you can install the dependencies, as mentioned before:

   .. code-block:: bash

      pip install -r requirements.txt

To Do
-----

This to-do list includes a list of all possible improvements and/or fixes.

- Add more password generating possibilities.
  This may be a never-ending item on the to-do list. Add more possibilities to add generate more passwords based on the seed words.

- Improve iteration in character replacement in password generating.
  Iteration does not always seem fully functional when replacing characters. Iteration is used to replace more than 1 type of character in a word. For example, a word 'word' can turn into 'w0rd' during the first iteration, and can turn into 'w0r)' during the second iteration. This works, but it seems there is little to no difference between 3 and 10 iterations, when it comes to the number of results. This requires some research.

- Add generating rules.
  The configuration holds some variables that can be used for password generating rules, to limit processing time, by limiting the number of passwords actually created, and allowing users to specify the type of passwords they expect. More rules should be added to improve this functionality.

- Add category support.
  There are a number of categories in a dedicated directory. These categories all hold a list of words that relate to these categories. More words should be added to all these categories and the scoring should parse all these word lists to see if any of these words exist in a given password, incrementing the score if so.

- Add pattern scoring.
  Pattern scoring can be useful for patterns such as birthdates, where it is not feasible to have a list of all possible birthdates to check against. The pattern can be used to check if the password (probably) has a birthdate embedded into it. If so, the score can be incremented.
