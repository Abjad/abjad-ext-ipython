#! /usr/bin/env python
import pathlib

import setuptools

subpackage_name = "ipython"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / "abjadext" / subpackage_name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


if __name__ == "__main__":
    setuptools.setup(
        author="Josiah Wolf Oberholtzer",
        author_email="josiah.oberholtzer@gmail.com",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Artistic Software",
        ],
        include_package_data=True,
        install_requires=[
            "abjad==3.3",
            "black",
            "flake8",
            "isort",
            "mypy",
            "pytest>=5.4.3",
            "pytest-helpers-namespace",
            "jupyter>=1.0.0",
        ],
        license="MIT",
        long_description=pathlib.Path("README.md").read_text(),
        keywords=", ".join(
            [
                "jupyter",
                "lilypond",
                "music composition",
                "music notation",
            ]
        ),
        name="abjad-ext-{}".format(subpackage_name),
        packages=["abjadext"],
        platforms="Any",
        url="http://abjad.github.io",
        version=read_version(),
    )
