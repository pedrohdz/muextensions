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
regebro/hovercraft#196 which adds the ``--directive-plugin`` argument to the
``hovercraft`` command.  The source code introducing ``--directive-plugin`` can
be found in `pedrohdz/hovercraft <PATCHED_>`_ under the ``directives`` branch.

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
