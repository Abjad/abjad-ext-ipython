import abjad
import abjadext.ipython
import pathlib
import pytest
import unittest.mock


def test_success():
    """
    Show can process illustrable objects.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('IPython.core.display.display_png') as display_mock:
        with unittest.mock.patch.object(
            show, '_run_imagemagick',
            wraps=show._run_imagemagick,
        ) as convert_mock:
            show(staff)
    assert convert_mock.call_count == 1
    assert display_mock.call_count == 1
    png_path = pathlib.Path(convert_mock.call_args[0][0])
    assert not png_path.exists()
    assert not png_path.parent.exists()


def test_multipage_success():
    staff = abjad.Staff("c'1 d'1 e'1 f'1")
    for leaf in staff[:-1]:
        abjad.attach(abjad.LilyPondLiteral(r'\pageBreak', 'after'), leaf)
    assert format(staff) == abjad.String.normalize(r'''
        \new Staff
        {
            c'1
            \pageBreak
            d'1
            \pageBreak
            e'1
            \pageBreak
            f'1
        }
    ''')
    show = abjadext.ipython.Show()
    with unittest.mock.patch('IPython.core.display.display_png') as display_mock:
        with unittest.mock.patch.object(
            show, '_run_imagemagick',
            wraps=show._run_imagemagick,
            ) as convert_mock:
            show(staff)
    assert convert_mock.call_count == 4
    assert display_mock.call_count == 4
    png_path = pathlib.Path(convert_mock.call_args_list[0][0][0])
    assert not png_path.exists()
    assert not png_path.parent.exists()


def test_no_illustrate_method():
    """
    Argument must be illustrable.
    """
    class Foo:
        pass
    foo = Foo()
    show = abjadext.ipython.Show()
    with pytest.raises(TypeError):
        show(foo)


def test_illustrate_failed():
    """
    Exceptions during illustration propagate out.
    """
    class Foo:
        def __illustrate__(self):
            raise ValueError("I can't actually be illustrated.")
    foo = Foo()
    show = abjadext.ipython.Show()
    with pytest.raises(ValueError) as excinfo:
        show(foo)
    assert "I can't actually be illustrated." in str(excinfo.value)


def test_lilypond_not_found():
    """
    Show will fail if LilyPond cannot be found.
    """
    def side_effect(name):
        return False
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjad.system.IOManager.find_executable') as mock:
        mock.side_effect = side_effect
        with pytest.raises(RuntimeError) as excinfo:
            show(staff)
        assert 'Cannot find LilyPond.' in str(excinfo.value)


def test_imagemagick_not_found():
    """
    Show will fail if ImageMagick cannot be found.
    """
    def side_effect(name):
        if name == 'convert':
            return False
        return True
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjad.system.IOManager.find_executable') as mock:
        mock.side_effect = side_effect
        with pytest.raises(RuntimeError) as excinfo:
            show(staff)
        assert 'Cannot find ImageMagick.' in str(excinfo.value)


def test_lilypond_failed():
    """
    Show will fail if LilyPond fails to render.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjad.system.PersistenceManager.as_png') as mock:
        mock.side_effect = RuntimeError('Who knew?')
        with pytest.raises(RuntimeError) as excinfo:
            show(staff)
        assert 'Who knew?' in str(excinfo.value)


def test_no_lilypond_output():
    """
    Show will fail if LilyPond output disappears.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjad.system.PersistenceManager.as_png') as mock:
        mock.return_value = ((), 0.0, 0.0, True)
        with pytest.raises(FileNotFoundError):
            show(staff)


def test_imagemagick_failed():
    """
    Show will fail if ImageMagick fails to render.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjadext.ipython.Show._run_imagemagick') as mock:
        mock.return_value = -1
        with pytest.raises(RuntimeError) as excinfo:
            show(staff)
        assert 'ImageMagick failed: -1' in str(excinfo.value)


def test_no_imagemagick_output():
    """
    Show will fail if ImageMagick output disappears.
    """
    def side_effect(png_path):
        pathlib.Path(png_path).unlink()
        return 0
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    show = abjadext.ipython.Show()
    with unittest.mock.patch('abjadext.ipython.Show._run_imagemagick') as mock:
        mock.side_effect = side_effect
        with pytest.raises(FileNotFoundError):
            show(staff)
