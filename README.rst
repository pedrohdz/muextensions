|Code Climate| |Build Status| |codecov| |PyPI version|

muextensions
============

Tasks:

1. Add ``plantuml-txt`` directive.

2. X - Connect to Pelican.

3. Add caching.

4. Add Ditaa (sp?)

5. Add REST callers for execs.


Layout:

muextensions/
  - contrib/ - Exports to allow plugging into this.
      - hovercraft/
          - plantuml-image
          - plantuml-txt
          - ditaa-image
          - ditaa-text
      - instantrst/
      - pelicanrst/
      - pelicanmd/
  - connector/ - What connects the _executors_ to the markup processors.
    - docutil/
    - markdown/
  - executor/ - Wrappers


.. |Code Climate| image:: https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg
   :target: https://codeclimate.com/github/pedrohdz/muextensions
.. |Build Status| image:: https://travis-ci.org/pedrohdz/muextensions.svg?branch=master
   :target: https://travis-ci.org/pedrohdz/muextensions
.. |codecov| image:: https://codecov.io/gh/pedrohdz/muextensions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pedrohdz/muextensions
.. |PyPI version| image:: https://badge.fury.io/py/muextensions.svg
   :target: https://badge.fury.io/py/muextensions
