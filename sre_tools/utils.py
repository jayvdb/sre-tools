from sre_parse import SubPattern, parse

try:
    from sre_parse import Pattern
except ImportError:
    from sre_parse import State as Pattern


def _subpattern_invoke(pattern, func):
    if not isinstance(pattern, SubPattern):
        pattern = parse(pattern)
    return pattern, func(pattern.data)


def clone_subpattern(subpattern, data=None):
    if not data:
        data = subpattern.data
    try:
        state = subpattern.state
    except AttributeError:
        state = subpattern.pattern
    return SubPattern(state, data)


def create_subpattern(seq=None):
    state = Pattern()
    return SubPattern(state, seq)
