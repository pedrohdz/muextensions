from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst import directives

from muextensions.executor.ditaa import DitaaWrapper
from . import Connector


class DitaaImageDirectiveBase(Connector, Image):
    required_arguments = 0
    has_content = True
    option_spec = Image.option_spec.copy()
    option_spec['basename'] = directives.unchanged
    option_spec['format'] = lambda _: directives.choice(_, ('png', 'svg'))

    # FIXME - Move to Connector.run()
    def run(self):
        image_format = self.options.get('format', self.default_image_format)

        # FIXME - Move to DitaaImageDirectiveBase.get_executor()
        executor = DitaaWrapper(self.content, output_format=image_format)

        basename = self.options.get('basename', executor.hashcode())
        target_path = self.target_dir.joinpath(basename) \
            .with_suffix('.' + image_format)
        if not target_path.parent.exists() and self.create_dirs:
            target_path.parent.mkdir(parents=True)

        # FIXME - Add docutils error handling!!!
        executor.write(target_path)

        if self.base_uri is not None:
            uri = '/'.join([self.base_uri, target_path.name])
        else:
            uri = str(target_path)

        self.arguments.append(uri)
        return super().run()


def register(target_dir, base_uri=None, default_image_format='png',
             create_dir=False):
    register_directive(
        'ditaa-image',
        build_ditaa_image_directive(
            target_dir, base_uri, default_image_format, create_dir))


def build_ditaa_image_directive(
        target_dir, base_uri, default_image_format, create_dir):
    return type('DitaaImageDirective',
                (DitaaImageDirectiveBase,),
                {'_target_dir': target_dir,
                 '_base_uri': base_uri,
                 '_default_image_format': default_image_format,
                 '_create_dirs': create_dir})
