#!/usr/bin/env python
import re
import ast
from setuptools import setup, find_packages


def version():
    version_re = re.compile(r'^\s*__version__\s*=\s*[\'"](.*)[\'"]')
    with open('muextentions/__init__.py', 'rb') as handle:
        return str(ast.literal_eval(version_re.search(
            handle.read().decode('utf-8')).group(1)))


def long_description():
    with open('README.rst', 'rb') as handle:
        return handle.read().decode('utf-8')


_TEST_REQUIRE = [
    # coverage 5 is still in alpha.
    'coverage<5',
    'pytest-cov',
    'pytest',
    # Optional external dependencies needed while testing.
    'docutils',
    'pelican',
]

_CI_REQUIRE = [
    'flake8',
    'pep257',
    'pylint',
    'tox',
]

setup(
    name='muextentions',
    # version=version(),
    author='Pedro H.',
    author_email='5179251+pedrohdz@users.noreply.github.com',
    description='Markup extentions',
    long_description=long_description(),
    url='https://github.com/pedrohdz/muextentions',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
    ],
    keywords='pelican hovercraft plantuml uml docutils',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
    ],
    tests_require=_TEST_REQUIRE,
    extras_require={
        'ci': _CI_REQUIRE,
        'test': _TEST_REQUIRE,
    },
)
