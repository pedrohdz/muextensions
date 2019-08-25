.. COMMENT_OUT

|Code Climate| |Build Status| |codecov| |PyPI version|

###############################################################################
muextensions
###############################################################################

.. contents:: Table of contents


Overview
===============================================================================
*This project is still in alpha.  Expect backwards compatibility breaking
changes.*

Adds `ditaa`_ and `PlantUML`_ directives to `reStructuredText`_, and hopefully
`Markdown`_ in the future.  *muextensions* does this by providing plugins for
projects like `Hovercraft! <Hovercraft_>`_ and `Pelican`_, and simplifies
registering the directives with other `Docutils`_ projects.

It allows for adding a *reStructuredText* block like the following:

.. code:: rst

  .. ditaa-image::

      +---------------+                      /---------------------+
      | +-----------+ |    +------------+    |+---+  +----+   /---+|
      | | ..dita::  | +--->+muextensions+--->+|   +->+{io}+-> +   ||
      | |   ~~~~~~~ | |    |        {io}|    ||{d}|  +----+   |   ||
      | |   ~~~~~~~ | |    +------------+    |+---+           +---/|
      | +-----------+ |                      |                     |
      |            {d}|                      |                     |
      +---------------+                      +---------------------/

And having it embedded in the `Docutils`_ generated document as an image:

.. image:: docs/images/simple-ditaa-example.svg
  :alt: Simple ditaa example
  :align: center


In the case of *PlantUML*, a block like:

.. code:: rst

  .. plantuml-image::

    skinparam monochrome true
    skinparam shadowing false

    client -> front_end
    front_end -> back_end
    back_end -> front_end
    front_end -> client

Would be rendered as:

.. image:: docs/images/simple-plantuml-example.svg
  :alt: Simple PlantUML example
  :align: center


Usage
===============================================================================

Prerequisites
-------------

Install `PlantUML`_ and have a wrapper script with the name ``plantuml`` that
executes it installed in your path for *PlantUML* support.  A sample wrapper
script is included in `contrib/scripts/plantuml <plantuml_wrapper_>`_ of this
project.

For `ditaa`_ support, install as described in the `Getting it <get_ditaa_>`_
section of the *ditaa* documentation.

.. _get_ditaa: https://github.com/stathissideris/ditaa#getting-it
.. _plantuml_wrapper: contrib/scripts/plantuml


Pelican
-------

*muextensions* provides a plugin for `Pelican`_ in
``muextensions.contrib.pelican``.

If everything is configured correctly, integrating *muextensions* into
*Pelican* should be as simple as:

1. Installing *muextensions* in the Python virtual environment that *Pelican*
   is installed in with:

   .. code:: bash

      pip install muextensions

2. Appending ``'muextensions.contrib.pelican'`` to ``PLUGINS`` in your
   ``pelicanconf.py``:

   .. code:: python

      PLUGINS = ['muextensions.contrib.pelican',]

For more information on how to configure plugins in *Pelican*, refer to the
`How to use plugins <pelican_plugins_>`_ section in their documentation.

.. _pelican_plugins: http://docs.getpelican.com/en/stable/plugins.html


Hovercraft!
-----------

Support for `Hovercraft! <Hovercraft_>`_ is currently pending pull request
`regebro/hovercraft#196 <hovercraft_pr_196_>`_
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

.. _Hovercraft: https://hovercraft.readthedocs.io/en/latest/
.. _PATCHED: https://github.com/pedrohdz/hovercraft/tree/directives


Other docutils projects
-----------------------

The *muextensions* *reStructuredText* directives can be added to any
`Docutils`_ project by way of *Docutils* *connectors* in
``muextensions.connector.docutils``.

.. code:: python

  from pathlib import Path
  from muextensions.connector.docutils import plantuml, ditaa

  output_path = Path('.')
  plantuml.register(output_path)
  ditaa.register(output_path)

The ``plantuml`` and ``ditaa`` ``register()`` functions in
``muextensions.connector.docutils`` handle registering the *reStructuredText*
directives as described in the `Register the Directive <docutils_register_>`_
section on the *Docutils* of the documentation.

.. _docutils_register: http://docutils.sourceforge.net/docs/howto/rst-directives.html#register-the-directive

.. _Docutils: http://docutils.sourceforge.net/index.html


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
- This project conforms to `Semantic Versioning 2.0.0 <semver_>`_.

.. _semver: https://semver.org/


Appendix
===============================================================================

Todo list
---------

- [X] Add Pelican support.
- [X] Add Ditaa support.
- [ ] Finish adding plugin support to Hovercraft!  (`regebro/hovercraft#196
  <hovercraft_pr_196_>`_).
- [ ] Add GitHub tickets for each of the following.
- [ ] Add caching.
- [ ] Add a ``plantuml-text`` directive.  This should generate and embed ASCII
  art by way of ``plantuml -ttxt``.
- [ ] Add a ``ditaa-text`` directive.  This should embed ASCII art in the
  directive contents directly as a ``code`` block.
- [ ] Add ``ditaa-figure`` and ``plantuml-figure`` directives the inherit from
  `figure
  <http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure>`_.
- [ ] Add REST callers for execs to speed things up even more.
- [ ] Finish removing the deprecated `uml` directive.
- [ ] Look into https://pypi.org/project/pbr/
- [ ] Add Markdown support.


References
----------

- *TODO*


.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _ditaa: https://github.com/stathissideris/ditaa
.. _PlantUML: http://plantuml.com/
.. _Markdown: https://daringfireball.net/projects/markdown/
.. _Hovercraft: https://hovercraft.readthedocs.io/en/latest/
.. _Pelican: http://docs.getpelican.com/en/stable/

.. _hovercraft_pr_196: https://github.com/regebro/hovercraft/pull/196

.. |Code Climate| image:: https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg
   :target: https://codeclimate.com/github/pedrohdz/muextensions
.. |Build Status| image:: https://travis-ci.org/pedrohdz/muextensions.svg?branch=master
   :target: https://travis-ci.org/pedrohdz/muextensions
.. |codecov| image:: https://codecov.io/gh/pedrohdz/muextensions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pedrohdz/muextensions
.. |PyPI version| image:: https://badge.fury.io/py/muextensions.svg
   :target: https://badge.fury.io/py/muextensions
