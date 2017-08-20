import abjad
import os
import subprocess
import tempfile
from IPython.core.display import display_png


class Graph:
    """
    IPython replacement callable for `abjad.graph()`.
    """

    ### SPECIAL METHODS ###

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
        elif hasattr(argument, '__graph__'):
            graphviz_graph = argument.__graph__(**keywords)
            if graph_attributes:
                graphviz_graph.attributes.update(graph_attributes)
            if node_attributes:
                graphviz_graph.node_attributes.update(node_attributes)
            if edge_attributes:
                graphviz_graph.edge_attributes.update(edge_attributes)
            graphviz_format = str(graphviz_graph)
        else:
            raise TypeError('Cannot illustrate {!r}'.format(type(argument)))
        valid_layouts = (
            'circo',
            'dot',
            'fdp',
            'neato',
            'osage',
            'sfdp',
            'twopi',
            )
        if layout not in valid_layouts:
            raise ValueError('Invalid layout: {}'.format(layout))
        if not abjad.IOManager.find_executable(layout):
            raise RuntimeError('Cannot find Graphviz.')
        if not abjad.IOManager.find_executable('convert'):
            raise RuntimeError('Cannot find ImageMagick.')
        with tempfile.TemporaryDirectory() as temporary_directory:
            dot_path = os.path.join(temporary_directory, 'graph.dot')
            pdf_path = os.path.join(temporary_directory, 'graph.pdf')
            png_path = os.path.join(temporary_directory, 'graph.png')
            with open(dot_path, 'w') as file_pointer:
                file_pointer.write(graphviz_format)
            command = '{} -v -Tpdf {} -o {}'
            command = command.format(layout, dot_path, pdf_path)
            exit_code = subprocess.call(command, shell=True)
            if exit_code:
                raise RuntimeError('Graphviz failed.')
            command = 'convert {} -trim {}'
            command = command.format(pdf_path, png_path)
            exit_code = subprocess.call(command, shell=True)
            if exit_code:
                raise RuntimeError('ImageMagick failed.')
            abjad.IOManager.spawn_subprocess(command)
            with open(png_path, 'rb') as file_pointer:
                png = file_pointer.read()
        display_png(png, raw=True)
