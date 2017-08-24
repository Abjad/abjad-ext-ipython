import abjad
import abjadext.ipython
import pathlib
import pytest
import unittest.mock


def test_success():
    """
    Play can process illustrable objects.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    play = abjadext.ipython.Play()
    with unittest.mock.patch('IPython.core.display.display_html') as display_mock:
        with unittest.mock.patch.object(
            play, '_run_timidity',
            wraps=play._run_timidity,
            ) as timidity_mock:
            play(staff)
    assert timidity_mock.call_count == 1
    assert display_mock.call_count == 1
    audio_path = pathlib.Path(timidity_mock.call_args[0][1])
    assert not audio_path.exists()
    assert not audio_path.parent.exists()


def test_no_illustrate_method():
    """
    Argument must be illustrable.
    """
    class Foo:
        pass
    foo = Foo()
    graph = abjadext.ipython.Graph()
    with pytest.raises(TypeError):
        graph(foo)


def test_illustrate_failed():
    pass


def test_lilypond_not_found():
    pass


def test_timidity_not_found():
    pass


def test_lilypond_failed():
    pass


def test_timidity_failed():
    pass


def test_no_lilypond_output():
    pass


def test_no_timidity_output():
    pass
