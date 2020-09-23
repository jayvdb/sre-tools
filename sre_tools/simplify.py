from sre_parse import SubPattern, parse

from .utils import clone_subpattern
from ._simplify import _simplify_sre_list


def simplify_regex(pattern):
    if not isinstance(pattern, SubPattern):
        pattern = parse(pattern)
    seq = _simplify_sre_list(pattern.data)
    return clone_subpattern(pattern, seq)
