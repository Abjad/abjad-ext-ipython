#! /usr/bin/env python
import setuptools


if __name__ == '__main__':
    setuptools.setup(
        install_requires=[],
        name='abjad-ext-ipython',
        namespace_packages=['abjad.ext'],
        packages=[
            'abjad.ext.ipython',
            ],
        )
