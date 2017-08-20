import abjad
import base64
import pathlib
import subprocess
import tempfile
import IPython.core.display


class Play(object):
    """
    IPython replacement callable for `abjad.play()`.

    Integrates audio rendering of Abjad MIDI files into IPython notebooks
    using `timidity`, and displays the resulting audio as an <audio> tag.
    """

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        if not abjad.IOManager.find_executable('lilypond'):
            raise RuntimeError('Cannot find LilyPond.')
        if not abjad.IOManager.find_executable('convert'):
            raise RuntimeError('Cannot find ImageMagick.')
        if not hasattr(argument, '__illustrate__'):
            raise TypeError('Cannot play {!r}'.format(type(argument)))
        has_vorbis = self._check_for_vorbis()
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory = pathlib.Path(temporary_directory)
            midi_file_path = temporary_directory / 'out.midi'
            result = abjad.persist(argument).as_midi(midi_file_path)
            midi_file_path, format_time, render_time = result
            if has_vorbis:
                audio_file_path = temporary_directory / 'out.ogg'
            else:
                audio_file_path = temporary_directory / 'out.aif'
            encoded_audio = self._get_audio_as_base64(
                midi_file_path,
                audio_file_path,
                has_vorbis,
                )
        if encoded_audio is not None:
            self._display_audio_tag(encoded_audio, has_vorbis)

    ### PRIVATE METHODS ###

    def _check_for_vorbis(self):
        has_vorbis = False
        output = subprocess.check_output('timidity --help', shell=True)
        output = output.decode('utf-8')
        for line in output.splitlines():
            for part in line.split():
                if part == '-Ov':
                    has_vorbis = True
                    break
        return has_vorbis

    def _display_audio_tag(self, encoded_audio, has_vorbis):
        if has_vorbis:
            mime_type = 'audio/ogg'
        else:
            mime_type = 'audio/aiff'
        audio_tag = '<audio controls type="{}" '
        audio_tag += 'src="data:{};base64,{}">'
        audio_tag = audio_tag.format(mime_type, mime_type, encoded_audio)
        IPython.core.display.display_html(audio_tag, raw=True)

    def _get_audio_as_base64(
        self,
        midi_file_path,
        audio_file_path,
        has_vorbis,
        ):
        if has_vorbis:
            output_flag = '-Ov'
        else:
            output_flag = '-Oa'
        command = 'timidity {midi_file_path} {output_flag} -o {audio_file_path}'.format(
            midi_file_path=midi_file_path,
            output_flag=output_flag,
            audio_file_path=audio_file_path,
            )
        exit_code = subprocess.call(command, shell=True)
        if exit_code:
            message = 'Timidity failed: {}'.format(exit_code)
            raise RuntimeError(message)
        encoded_audio = self._get_base64_from_file(audio_file_path)
        return encoded_audio

    def _get_base64_from_file(self, file_name):
        with open(str(file_name), 'rb') as file_pointer:
            data = file_pointer.read()
            return base64.b64encode(data).decode('utf-8')
