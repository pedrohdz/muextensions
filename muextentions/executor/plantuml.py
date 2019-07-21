#! /use/bin/env python
# pylint: disable=missing-docstring

import hashlib
import itertools
import logging
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from .executer import execute, ExecutionError


LOG = logging.getLogger(__name__)


class PlantUmlWrapper():
    def __init__(self,
                 uml_body,
                 output_format='svg',
                 encoding='utf-8',
                 timeout=30):
        try:
            iter(uml_body)
        except TypeError:
            raise TypeError('"uml_body" must be iterable')

        if output_format not in ('png', 'svg'):
            raise ValueError('"output_format" must be one of: png, svg')

        self._uml_body = uml_body
        self._format = output_format
        self._encoding = encoding
        self._timeout = timeout
        self._log = logging.getLogger(type(self).__name__)

    def write(self, output_file):
        with TemporaryDirectory(prefix='muextentions-plantuml-') as work_dir:
            self._process(work_dir, output_file)

    def hashcode(self):
        hasher = hashlib.md5()
        for item in self._uml_iterator():
            hasher.update(item)
        return hasher.hexdigest()

    def _process(self, work_dir, output_file):
        base_name = self.hashcode()
        puml_path = Path(work_dir, base_name).with_suffix('.puml')
        self._write_uml_file(puml_path)
        output_path = self._execute_plantuml(puml_path)
        self._log.debug('Moving "%s" to "%s".', output_path, output_file)
        shutil.move(output_path, output_file)

    def _execute_plantuml(self, puml_path):
        option = '-t{}'.format(self._format)
        execute(['plantuml', option, puml_path])
        output_path = puml_path.with_suffix('.' + self._format)
        if not output_path.exists():
            raise ExecutionError('Failed to create "{}"'.format(output_path))
        return output_path

    def _uml_iterator(self):
        data = itertools.chain(['@startuml'], self._uml_body, ['@enduml'])
        return ('{}\n'.format(line).encode(self._encoding) for line in data)

    def _write_uml_file(self, puml_path):
        with open(puml_path, 'bw+') as handle:
            for line in self._uml_iterator():
                handle.write(line)


def main():
    wrapper = PlantUmlWrapper(['Bob->Alice : hello'])
    wrapper.write('foo')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
