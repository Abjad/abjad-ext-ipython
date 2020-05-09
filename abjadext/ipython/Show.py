import pathlib
import subprocess
import tempfile

import IPython.core.display  # type: ignore
import abjad

from wand.image import Image as WImage


class Show:
    """
    IPython replacement callable for `abjad.show()`.
    """

    # ### SPECIAL METHODS ### #

    def __call__(self, argument):
        if not hasattr(argument, "__illustrate__"):
            raise TypeError("Cannot illustrate {!r}".format(type(argument)))
        if not abjad.IOManager.find_executable("lilypond"):
            raise RuntimeError("Cannot find LilyPond.")
        if not abjad.IOManager.find_executable("convert"):
            raise RuntimeError("Cannot find ImageMagick.")
        if not abjad.IOManager.find_executable("pdfcrop"):
            raise RuntimeError("Cannot find PDFCrop")
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory = pathlib.Path(temporary_directory)
            temporary_file_path = temporary_directory / "output.pdf"
            pdf_path, _, _, success = abjad.persist(argument).as_pdf(
                str(temporary_file_path)
            )
            if not success:
                raise RuntimeError("Rendering failed")
            if pdf_path is None:
                raise FileNotFoundError("LilyPond PDF output not found.")
            self._run_pdfcrop(pdf_path)
            with WImage(filename=pdf_path, resolution=100) as img:
                img.format="png"
                png_path = pathlib.Path(pdf_path).with_suffix('.png')
                img.save(filename=png_path)
                with open(str(png_path), "rb") as file_pointer:
                    file_contents = file_pointer.read()
                    IPython.core.display.display_png(file_contents, raw=True)
        #    for pdf_path in pdf_paths:
        #        print(pdf_path)
        #        png_path = pathlib.Path(pdf_path).with_suffix(".png")
        #        exit_code = self._run_imagemagick(pdf_path)
        #        if exit_code:
        #            message = "ImageMagick failed: {}".format(exit_code)
        #            raise RuntimeError(message)
        #        with open(str(pdf_path), "rb") as file_pointer:
        #            file_contents = file_pointer.read()
        #            pngs.append(file_contents)
        #for png in pngs:
        #    IPython.core.display.display_png(png, raw=True)

    # ### PRIVATE METHODS ### #

    def _run_imagemagick(self, png_path):
        command = "convert {png_path} -trim {png_path}"
        command = command.format(png_path=png_path)
        return subprocess.call(command, shell=True)

    def _run_pdfcrop(self, pdf_path):
        command = "pdfcrop --hires {pdf_path} {pdf_path}"
        command = command.format(pdf_path=pdf_path)
        return subprocess.call(command, shell=True)
