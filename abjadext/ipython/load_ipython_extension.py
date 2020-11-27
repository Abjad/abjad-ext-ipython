import subprocess

from abjad.io import AbjadGrapher, Illustrator, Player


def load_ipython_extension(ipython):
    """
    Integrates audio and visual rendering of Abjad scores in IPython notebooks.

    This extension requires `timidity` be in your $PATH. If you do not have
    `timidity` installed, it is likely available in your platform's package
    manager:

    On OSX::

        ~$ brew install timidity

    On Debian or Ubuntu:

        ~$ apt-get install timidity

    To activate the IPython notebook extension, add the following line in your
    notebook:

        %load_ext abjadext.ipython

    """
    patch_graph(ipython)
    patch_play(ipython)
    patch_show(ipython)


def display_audio(midi_path):
    from IPython.core.display import display
    from IPython.display import Audio

    audio_path = midi_path.with_suffix(".ogg")
    command = f"timidity {midi_path} -Ov -o {audio_path}"
    subprocess.run(command, shell=True, check=True)
    display(Audio(filename=str(audio_path)))


def display_svg(output_path):
    from IPython.core.display import display_svg

    with output_path.open() as file_pointer:
        contents = file_pointer.read()
    display_svg(contents, raw=True)


def patch_graph(ipython):
    def get_format(self):
        return "svg"

    def open_output_path(self, output_path):
        display_svg(output_path)

    AbjadGrapher.get_format = get_format
    AbjadGrapher.open_output_path = open_output_path


def patch_play(ipython):
    def open_output_path(self, output_path):
        display_audio(output_path)

    Player.open_output_path = open_output_path


def patch_show(ipython):
    def get_openable_paths(self, output_paths):
        for path in output_paths:
            if path.name.endswith(".cropped.svg"):
                yield path

    def open_output_path(self, output_path):
        display_svg(output_path)

    def get_render_command(self, input_path, lilypond_path):
        parts = [
            str(lilypond_path),
            "-dbackend=svg",
            "-dcrop",
            "-dno-point-and-click",
            "-o",
            str(input_path.with_suffix("")),
            str(input_path),
        ]
        return " ".join(parts)

    Illustrator.get_openable_paths = get_openable_paths
    Illustrator.get_render_command = get_render_command
    Illustrator.open_output_path = open_output_path
