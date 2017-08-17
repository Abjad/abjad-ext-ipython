#! /usr/bin/env python
import setuptools


if __name__ == '__main__':
    setuptools.setup(
        install_requires=[
            'abjad==2.21',
            ],
        name='abjad-ext-ipython',
        namespace_packages=['abjad.ext'],
        packages=[
            'abjad.ext.ipython',
            ],
        )
