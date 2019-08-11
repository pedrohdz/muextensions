.. COMMENT_OUT

|Code Climate| |Build Status| |codecov| |PyPI version|

###############################################################################
muextensions
###############################################################################

.. contents:: Table of contents


Usage
===============================================================================

Prerequisites
-------------

Install `PlantUML`_ and have a wrapper script with the name ``plantuml`` that
executes it installed in your path.  A sample wrapper script is included in
`contrib/scripts/plantuml <plantuml_wrapper_>`_ of this project.

.. _plantuml_wrapper: contrib/scripts/plantuml
.. _PlantUML: http://plantuml.com/


Hovercraft!
-----------

Support for `Hovercraft! <HOVERCRAFT_>`_ is currently pending pull request
`regebro/hovercraft#196 <https://github.com/regebro/hovercraft/pull/196>`_
which adds the ``--directive-plugin`` argument to the ``hovercraft`` command.
The source code introducing ``--directive-plugin`` can be found in
`pedrohdz/hovercraft <PATCHED_>`_ under the ``directives`` branch.

Here is a quick example to see *muextensions*, make sure to complete the
`Prerequisites`_ first.  We will utilize the demo presentation in
`docs/examples/hovercraft/ <docs/examples/hovercraft/>`_.

.. code:: bash

  cd docs/examples/hovercraft/
  python3.7 -m venv .venv
  source .venv/bin/activate
  pip install -U pip
  pip install muextensions \
      https://github.com/pedrohdz/hovercraft/archive/directives.zip
  hovercraft --directive-plugin muextensions.contrib.hovercraft demo.rst

Open http://localhost:8000/ in a web browser to see the *Hovercraft!*
presentation.


.. _HOVERCRAFT: https://hovercraft.readthedocs.io/en/latest/
.. _PATCHED: https://github.com/pedrohdz/hovercraft/tree/directives


Pelican
-------

*Coming soon*



Development
===============================================================================

Setting up for development:

.. code:: bash

  git clone git@github.com:pedrohdz/muextensions.git
  cd muextensions
  python3.5 -m venv .venv
  source .venv/bin/activate
  pip install -U pip
  pip install -e .[ci,test]


Make sure you have a good baseline by running ``tox``.  Executing ``tox`` from
within a *venv* (Python virtual environments) will cause ``pip`` related errors
during the tests, either exit the *venv* via the ``deactivate`` command, or
execute ``tox`` from a new terminal.

.. code:: bash

  deactivate
  tox
  source .venv/bin/activate

To execute the unit tests:

.. code:: bash

  pytest

To execute and view the unit test code coverage:

.. code:: bash

  pytest --cov-report=html --cov
  open htmlcov/index.html

To run the integration tests, assuming both ``ditaa`` and ``plantuml`` are
installed on the system, use the ``--run-integration`` option.  To save the
output of the integration tests for examination, add the
``--save-integration-output-to`` option:

.. code:: bash

  pytest --run-integration
  pytest --run-integration --save-integration-output-to=./tmp


Contribution
------------

When contributing, please keep in mind the following before submitting the pull
request:

- Make sure that the ``tox`` checks complete without failure.
- When making code changes, add relevant unit tests.
- If fixing a bug, please try and add a regression test.  It should fail before
  the fix is applies, and pas after.


Appendix
===============================================================================

Todo list
---------

1. Add ``plantuml-txt`` directive.

2. X - Connect to Pelican.

3. Add caching.

4. Add Ditaa (sp?)

5. Add REST callers for execs.

6. Look into https://pypi.org/project/pbr/


References
----------

- *TODO*


.. |Code Climate| image:: https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg
   :target: https://codeclimate.com/github/pedrohdz/muextensions
.. |Build Status| image:: https://travis-ci.org/pedrohdz/muextensions.svg?branch=master
   :target: https://travis-ci.org/pedrohdz/muextensions
.. |codecov| image:: https://codecov.io/gh/pedrohdz/muextensions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pedrohdz/muextensions
.. |PyPI version| image:: https://badge.fury.io/py/muextensions.svg
   :target: https://badge.fury.io/py/muextensions
