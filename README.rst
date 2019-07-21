|Code Climate| |Build Status| |codecov| |PyPI version|

muextentions
============

Tasks:

1. Add ``plantuml-txt`` directive.

2. X - Connect to Pelican.

3. Add caching.

4. Add Ditaa (sp?)

5. Add REST callers for execs.


Layout:

muextentions/
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
   :target: https://codeclimate.com/github/pedrohdz/muextentions
.. |Build Status| image:: https://travis-ci.org/pedrohdz/muextentions.svg?branch=master
   :target: https://travis-ci.org/pedrohdz/muextentions
.. |codecov| image:: https://codecov.io/gh/pedrohdz/muextentions/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pedrohdz/muextentions
.. |PyPI version| image:: https://badge.fury.io/py/muextentions.svg
   :target: https://badge.fury.io/py/muextentions
