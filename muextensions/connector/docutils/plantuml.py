# pylint: disable=missing-docstring
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from muextensions.executor.plantuml import PlantUmlWrapper
from . import Connector


class PlantUmlDocutilsDirectiveBase(Connector, Directive):
    # FIXME - Make like `DitaaImageDirectiveBase`!
    # Potential template for this:
    #   - http://docutils.sourceforge.net/docs/howto/rst-directives.html
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        # image node options
        'align': lambda _: directives.choice(_, ('left', 'center', 'right')),
        'alt': directives.unchanged,
        'class': directives.class_option,
        'height': directives.nonnegative_int,
        'scale': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        # custom options
        'basename': directives.unchanged,
        'format': lambda _: directives.choice(_, ('png', 'svg'))
    }

    def run(self):
        plantuml_format = self.options.get('format', 'png')
        executor = PlantUmlWrapper(
            self.content,
            output_format=plantuml_format
        )

        basename = self.options.get('basename', executor.hashcode())
        file_name = '.'.join([basename, plantuml_format])
        target_path = Path(self.target_dir, file_name)
        if not target_path.parent.exists() and self.create_dirs:
            target_path.parent.mkdir(parents=True)

        executor.write(target_path)

        if self.base_uri is not None:
            self.options['uri'] = '/'.join([self.base_uri, target_path.name])
        else:
            self.options['uri'] = target_path

        image_node = nodes.image(rawsource=self.block_text, **self.options)
        return [image_node]


def register(target_dir, base_uri=None, create_dir=False):
    directive_class = type('PlantUmlDocutilsDirective',
                           (PlantUmlDocutilsDirectiveBase,),
                           {'_target_dir': target_dir,
                            '_base_uri': base_uri,
                            '_create_dirs': create_dir})
    directives.register_directive('plantuml-image', directive_class)

    # TODO - Depricate the `plantuml` directive in favor of `plantuml-image`.
    directives.register_directive('plantuml', directive_class)
