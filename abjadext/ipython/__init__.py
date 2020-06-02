"""
Abjad's IPython extension package.
"""
from ._version import __version__, __version_info__
from .load_ipython_extension import load_ipython_extension

__all__ = [
    "__version__",
    "__version_info__",
    "load_ipython_extension",
]
