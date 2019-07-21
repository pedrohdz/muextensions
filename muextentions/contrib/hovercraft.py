import os
import logging

from muextentions.connector.docutils import plantuml


BUILD_PATH = '_generated'


def register(args):
    # FIXME - Delete log config
    logging.basicConfig(level=logging.DEBUG)

    generate_dir = os.path.join(args.targetdir, BUILD_PATH)
    plantuml.register(generate_dir, BUILD_PATH, True)
