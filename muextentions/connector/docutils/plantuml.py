# pylint: disable=missing-docstring
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from muextentions.executor.plantuml import PlantUmlWrapper


def align_choice(argument):
    return directives.choice(argument, ('left', 'center', 'right'))


def format_choice(argument):
    return directives.choice(argument, ('png', 'svg'))


class PlantUmlDocutilsDirectiveBase(Directive):
    # pylint: disable=line-too-long, too-few-public-methods
    # Potential template for this:
    #   - https://github.com/getpelican/pelican-plugins/blob/master/plantuml/plantuml_rst.py#L22  # NOQA
    #   - http://docutils.sourceforge.net/docs/howto/rst-directives.html
    # pylint: enable=line-too-long
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        # image node options
        'align': align_choice,
        'alt': directives.unchanged,
        'class': directives.class_option,
        'height': directives.nonnegative_int,
        'scale': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        # custom options
        'basename': directives.unchanged,
        'format': format_choice,
    }

    @property
    def target_dir(self):
        # pylint: disable=no-member
        return self._target_dir

    @property
    def base_uri(self):
        # pylint: disable=no-member
        return self._base_uri

    @property
    def create_dirs(self):
        # pylint: disable=no-member
        return self._create_dirs

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
    directives.register_directive('plantuml', directive_class)
