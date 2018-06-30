import abjad
import pathlib
import subprocess
import tempfile
import IPython.core.display  # type: ignore


class Show:
    """
    IPython replacement callable for `abjad.show()`.
    """

    # ### SPECIAL METHODS ### #

    def __call__(self, argument):
        if not hasattr(argument, '__illustrate__'):
            raise TypeError('Cannot illustrate {!r}'.format(type(argument)))
        if not abjad.IOManager.find_executable('lilypond'):
            raise RuntimeError('Cannot find LilyPond.')
        if not abjad.IOManager.find_executable('convert'):
            raise RuntimeError('Cannot find ImageMagick.')
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory = pathlib.Path(temporary_directory)
            temporary_file_path = temporary_directory / 'output.png'
            png_paths, _, _, success = abjad.persist(argument).as_png(
                str(temporary_file_path))
            pngs = []
            if not success:
                raise RuntimeError('Rendering failed')
            if not png_paths:
                raise FileNotFoundError('LilyPond PNG output not found.')
            for png_path in png_paths:
                exit_code = self._run_imagemagick(png_path)
                if exit_code:
                    message = 'ImageMagick failed: {}'.format(exit_code)
                    raise RuntimeError(message)
                with open(str(png_path), 'rb') as file_pointer:
                    file_contents = file_pointer.read()
                    pngs.append(file_contents)
        for png in pngs:
            IPython.core.display.display_png(png, raw=True)

    # ### PRIVATE METHODS ### #

    def _run_imagemagick(self, png_path):
        command = 'convert {png_path} -trim {png_path}'
        command = command.format(png_path=png_path)
        return subprocess.call(command, shell=True)
