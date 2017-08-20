#! /usr/bin/env python
import pathlib
import setuptools


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path.join('abjadext', 'ipython', 'version.py')
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    version = local_dict['version']
    return version


author = 'Josiah Wolf Oberholtzer'

author_email = 'josiah.oberholtzer@gmail.com'

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Artistic Software',
    ]

install_requires = [
    'abjad>=2.21',
    'jupyter==1.0.0',
    ]

keywords = [
    'music composition',
    'music notation',
    'formalized score control',
    'lilypond',
    ]
keywords += [
    'documentation',
    'ipython',
    ]
keywords = ', '.join(keywords)

with open('README.rst', 'r') as file_pointer:
    long_description = file_pointer.read()

version = read_version()


if __name__ == '__main__':
    setuptools.setup(
        author=author,
        author_email=author_email,
        classifiers=classifiers,
        include_package_data=True,
        install_requires=install_requires,
        license='MIT',
        long_description=long_description,
        keywords=keywords,
        name='abjad-ext-ipython',
        packages=['abjadext'],
        platforms='Any',
        url='http://www.projectabjad.org',
        version=version,
        )
