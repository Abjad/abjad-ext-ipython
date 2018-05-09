import abjad
import copy
import pathlib
import subprocess
import tempfile
import uqbar.graphs
import IPython.core.display  # type: ignore


class Graph:
    """
    IPython replacement callable for `abjad.graph()`.
    """

    # ### CLASS VARIABLES ### #

    _valid_layouts = (
        'circo',
        'dot',
        'fdp',
        'neato',
        'osage',
        'sfdp',
        'twopi',
        )

    # ### SPECIAL METHODS ### #

    def __call__(
        self,
        argument,
        layout='dot',
        graph_attributes=None,
        node_attributes=None,
        edge_attributes=None,
        **keywords
    ):
        if isinstance(argument, str):
            graphviz_format = argument
        else:
            if hasattr(argument, '__graph__'):
                graphviz_graph = argument.__graph__(**keywords)
            elif isinstance(argument, uqbar.graphs.Graph):
                graphviz_graph = copy.deepcopy(argument)
            else:
                raise TypeError('Cannot graph {!r}'.format(type(argument)))
            if graph_attributes:
                graphviz_graph.attributes.update(graph_attributes)
            if node_attributes:
                graphviz_graph.node_attributes.update(node_attributes)
            if edge_attributes:
                graphviz_graph.edge_attributes.update(edge_attributes)
            graphviz_format = format(graphviz_graph, 'graphviz')

        if layout not in self._valid_layouts:
            raise ValueError('Invalid layout: {}'.format(layout))
        if not abjad.IOManager.find_executable(layout):
            raise RuntimeError('Cannot find Graphviz.')
        if not abjad.IOManager.find_executable('convert'):
            raise RuntimeError('Cannot find ImageMagick.')

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory = pathlib.Path(temporary_directory)
            dot_path = temporary_directory / 'graph.dot'
            pdf_path = temporary_directory / 'graph.pdf'
            png_path = temporary_directory / 'graph.png'
            with open(str(dot_path), 'w') as file_pointer:
                file_pointer.write(graphviz_format)
            exit_code = self._run_graphviz(layout, dot_path, pdf_path)
            if exit_code:
                message = 'Graphviz failed: {}'.format(exit_code)
                raise RuntimeError(message)
            if not pdf_path.exists():
                raise FileNotFoundError(str(pdf_path))
            exit_code = self._run_imagemagick(pdf_path, png_path)
            if exit_code:
                message = 'ImageMagick failed: {}'.format(exit_code)
                raise RuntimeError(message)
            with open(str(png_path), 'rb') as file_pointer:
                png = file_pointer.read()

        IPython.core.display.display_png(png, raw=True)

    # ### PRIVATE METHODS ### #

    def _run_graphviz(self, layout, dot_path, pdf_path):
        command = '{} -v -Tpdf {} -o {}'
        command = command.format(layout, dot_path, pdf_path)
        return subprocess.call(command, shell=True)

    def _run_imagemagick(self, pdf_path, png_path):
        command = 'convert {} -trim {}'
        command = command.format(pdf_path, png_path)
        return subprocess.call(command, shell=True)
