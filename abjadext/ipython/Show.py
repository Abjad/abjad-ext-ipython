import abjad
import pathlib
import subprocess
import tempfile
from IPython.core.display import display_png


class Show:
    """
    IPython replacement callable for `abjad.show()`.
    """

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        if not abjad.IOManager.find_executable('lilypond'):
            raise RuntimeError('Cannot find LilyPond.')
        if not abjad.IOManager.find_executable('convert'):
            raise RuntimeError('Cannot find ImageMagick.')
        if not hasattr(argument, '__illustrate__'):
            raise TypeError('Cannot illustrate {!r}'.format(type(argument)))
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory = pathlib.Path(temporary_directory)
            temporary_file_path = temporary_directory / 'output.png'
            result = abjad.persist(argument).as_png(temporary_file_path)
            pngs = []
            for file_path in result[0]:
                command = 'convert {file_path} -trim {file_path}'
                command = command.format(file_path=file_path)
                exit_code = subprocess.call(command, shell=True)
                if exit_code:
                    message = 'ImageMagick failed: {}'.format(exit_code)
                    raise RuntimeError(message)
                with open(str(file_path), 'rb') as file_pointer:
                    file_contents = file_pointer.read()
                    pngs.append(file_contents)
        for png in pngs:
            display_png(png, raw=True)
