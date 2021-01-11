from .utils import _subpattern_invoke, clone_subpattern
from ._simplify import _simplify_sre_list


def simplify_regex(pattern):
    pattern, seq = _subpattern_invoke(pattern, _simplify_sre_list)
    return clone_subpattern(pattern, seq)
