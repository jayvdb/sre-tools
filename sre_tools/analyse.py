from .utils import _subpattern_invoke
from ._analyse import preprocess


def check_regex(pattern):
    _, rv = _subpattern_invoke(pattern, preprocess)
    return list(rv)
