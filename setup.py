#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pony'
]

test_requirements = [
    'pytest'
]

setup(
    name='realms',
    version='0.0.0',
    description="A web game similar to the game Star Realms by White Wizard Games",
    long_description=readme + '\n\n' + history,
    author="Zach Mitchell",
    author_email='zmitchell@fastmail.com',
    url='https://github.com/zmitchell/realms',
    packages=[
        'realms',
    ],
    package_dir={'realms':
                 'realms'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='realms',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'realms = realms.__main__:main'
        ]
    }
)
