Markup Extentions
=================

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

