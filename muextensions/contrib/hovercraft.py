from pathlib import Path

from muextensions.connector.docutils import plantuml, ditaa


BUILD_PATH = '_generated'


def register(args):
    generate_dir = Path(args.targetdir).joinpath(BUILD_PATH)
    plantuml.register(
        target_dir=generate_dir,
        base_uri=BUILD_PATH,
        create_dir=True)
    ditaa.register(
        target_dir=generate_dir,
        base_uri=BUILD_PATH,
        create_dir=True)
