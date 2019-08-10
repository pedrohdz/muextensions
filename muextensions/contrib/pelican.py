from pathlib import Path
import os

from pelican import signals, logger

from muextensions.connector.docutils import plantuml, ditaa


BUILD_PATH = '_generated'


def pelican_init(pelicanobj):
    target_dir = os.path.join('images', BUILD_PATH)
    base_uri = '/' + target_dir
    output_path = Path(pelicanobj.settings['OUTPUT_PATH'])
    generate_dir = output_path.joinpath(target_dir)
    logger.info('Registered "%s" with working directory "%s" '
                'and a base URL of "%s"', __name__, generate_dir, base_uri)
    plantuml.register(
        target_dir=generate_dir,
        base_uri=base_uri,
        create_dir=True)
    ditaa.register(
        target_dir=generate_dir,
        base_uri=base_uri,
        create_dir=True)


def register():
    signals.initialized.connect(pelican_init)
