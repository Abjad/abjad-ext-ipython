def load_ipython_extension(ipython):
    '''
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

    '''
    import abjad
    from abjadext import ipython as abjad_ipython
    play = abjad_ipython.Play()
    show = abjad_ipython.Show()
    graph = abjad_ipython.Graph()
    abjad.play = play
    abjad.show = show
    abjad.graph = graph
    abjad.topleveltools.play = play
    abjad.topleveltools.show = show
    abjad.topleveltools.graph = graph
    names = {
        'play': play,
        'show': show,
        'graph': graph,
        }
    ipython.push(names)
