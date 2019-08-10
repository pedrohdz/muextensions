# pylint: disable=missing-docstring

import io
import hashlib
import logging
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from . import execute


LOG = logging.getLogger(__name__)


class DitaaWrapper():
    def __init__(self,
                 ditaa_body,
                 output_format='svg',
                 encoding='utf-8',
                 timeout=30):
        try:
            iter(ditaa_body)
        except TypeError:
            raise TypeError('"ditaa_body" must be iterable')

        if output_format not in ('png', 'svg'):
            raise ValueError(
                '"output_format" must be one of "png", "svg".  The following '
                'is unknown: {}'.format(output_format))

        self._ditaa_body = ditaa_body
        self._format = output_format
        self._encoding = encoding
        self._timeout = timeout
        self._log = logging.getLogger(type(self).__name__)

    @classmethod
    def from_file(cls, file_path, *args, encoding='utf-8', **kwargs):
        with io.open(str(file_path), 'r', encoding=encoding) as file:
            lines = [l.strip() for l in file.readlines()]
        return cls(lines, encoding=encoding, *args, **kwargs)

    def write(self, output_file):
        with TemporaryDirectory(prefix='muextensions-ditaa-') as work_dir:
            self._process(work_dir, output_file)

    def hashcode(self):
        hasher = hashlib.md5()
        for item in self._ditaa_iterator():
            hasher.update(item)
        return hasher.hexdigest()

    def _process(self, work_dir, output_file):
        base_name = self.hashcode()
        ditaa_path = Path(work_dir, base_name).with_suffix('.ditaa')
        self._write_ditaa_file(ditaa_path)
        output_path = self._execute_ditaa(ditaa_path)
        self._log.debug('Moving "%s" to "%s".', output_path, output_file)
        shutil.move(str(output_path), str(output_file))

    def _execute_ditaa(self, input_path):
        output_path = input_path.with_suffix('.' + self._format)
        command = ['ditaa', str(input_path), str(output_path)]
        command.extend(self._get_options())
        execute(command)
        if not output_path.exists():
            raise FileNotFoundError(
                'Failed to create "{}"'.format(output_path))
        return output_path

    def _get_options(self):
        options = []
        if self._format == 'svg':
            options.append('--svg')
        return options

    def _ditaa_iterator(self):
        return ('{}\n'.format(line).encode(self._encoding) for line in
                self._ditaa_body)

    def _write_ditaa_file(self, ditaa_path):
        with ditaa_path.open('bw+') as handle:
            for line in self._ditaa_iterator():
                handle.write(line)
