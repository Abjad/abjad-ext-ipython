import abjad
import abjadext.ipython
import pathlib
import pytest
import unittest.mock


def test_success():
    """
    Graph can process graphable objects.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('IPython.core.display.display_png') as display_mock:
        with unittest.mock.patch.object(
            graph, '_run_imagemagick',
            wraps=graph._run_imagemagick,
            ) as convert_mock:
            graph(staff)
    assert convert_mock.call_count == 1
    assert display_mock.call_count == 1
    png_path = pathlib.Path(convert_mock.call_args[0][0])
    assert not png_path.exists()
    assert not png_path.parent.exists()


def test_no_graph_method():
    """
    Argument must be graphable.
    """
    class Foo:
        pass
    foo = Foo()
    graph = abjadext.ipython.Graph()
    with pytest.raises(TypeError):
        graph(foo)


def test_invalid_layout():
    """
    Graph errors when passed an invalid layout.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with pytest.raises(ValueError):
        graph(staff, layout='invalid')


def test_graph_failed():
    """
    Exceptions during graphing propagate out.
    """
    class Foo:
        def __graph__(self):
            raise ValueError("I can't actually be graphed.")
    foo = Foo()
    graph = abjadext.ipython.Graph()
    with pytest.raises(ValueError) as excinfo:
        graph(foo)
    assert "I can't actually be graphed." in str(excinfo.value)


def test_graphviz_not_found():
    pass
    """
    Graph will fail if Graphviz cannot be found.
    """
    def side_effect(name):
        return False
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjad.system.IOManager.find_executable') as mock:
        mock.side_effect = side_effect
        with pytest.raises(RuntimeError) as excinfo:
            graph(staff)
        assert 'Cannot find Graphviz.' in str(excinfo.value)


def test_imagemagick_not_found():
    """
    Graph will fail if ImageMagick cannot be found.
    """
    def side_effect(name):
        if name == 'convert':
            return False
        return True
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjad.system.IOManager.find_executable') as mock:
        mock.side_effect = side_effect
        with pytest.raises(RuntimeError) as excinfo:
            graph(staff)
        assert 'Cannot find ImageMagick.' in str(excinfo.value)


def test_graphviz_failed():
    """
    Graph will fail if Graphviz fails to render.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjadext.ipython.Graph._run_graphviz') as mock:
        mock.return_value = -1
        with pytest.raises(RuntimeError) as excinfo:
            graph(staff)
        assert 'Graphviz failed: -1' in str(excinfo.value)


def test_imagemagick_failed():
    """
    Graph will fail if ImageMagick fails to render.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjadext.ipython.Graph._run_imagemagick') as mock:
        mock.return_value = -1
        with pytest.raises(RuntimeError) as excinfo:
            graph(staff)
        assert 'ImageMagick failed: -1' in str(excinfo.value)


def test_no_graphviz_output():
    """
    Graph will fail if Graphviz output disappears.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjadext.ipython.Graph._run_graphviz') as mock:
        mock.return_value = 0  # Don't produce the PDF
        with pytest.raises(FileNotFoundError):
            graph(staff)


def test_no_imagemagick_output():
    """
    Graph will fail if ImageMagick output disappears.
    """
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    graph = abjadext.ipython.Graph()
    with unittest.mock.patch('abjadext.ipython.Graph._run_imagemagick') as mock:
        mock.return_value = 0  # Don't produce the PNG
        with pytest.raises(FileNotFoundError):
            graph(staff)
