import os

from pelican import signals, logger

from muextentions.connector.docutils import plantuml


BUILD_PATH = '_generated'


def pelican_init(pelicanobj):
    target_dir = os.path.join('images', BUILD_PATH)
    base_uri = '/' + target_dir
    output_path = pelicanobj.settings['OUTPUT_PATH']
    generate_dir = os.path.join(output_path, target_dir)
    logger.info('Registered "%s" with working directory "%s" '
                'and a base URL of "%s"', __name__, generate_dir, base_uri)
    plantuml.register(generate_dir, base_uri, True)


def register():
    signals.initialized.connect(pelican_init)
