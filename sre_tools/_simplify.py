from sre_constants import _NamedIntConstant
from sre_parse import (
    ANY,
    IN,
    LITERAL,
    MAX_REPEAT,
    MAXREPEAT,
    SubPattern,
    SUBPATTERN,
)

from .utils import create_subpattern


def _simplify_sre_list(seq):
    new = []

    prev_tok = None
    prev_val = None
    for i, (tok, val) in enumerate(list(seq)):
        if tok == prev_tok and (val == prev_val or _val_eq(val, prev_val)):
            if tok == MAX_REPEAT:
                min_repeat = min(MAXREPEAT, prev_val[0] + val[0])
                max_repeat = min(MAXREPEAT, prev_val[1] + val[1])
                prev_val = min_repeat, max_repeat, prev_val[2]
                new[-1] = prev_tok, prev_val
                continue
            elif tok in (LITERAL, ANY, IN):
                prev_tok = MAX_REPEAT
                prev_val = (2, 2, create_subpattern([(tok, val)]))
                new[-1] = prev_tok, prev_val
                continue
        else:
            if tok == LITERAL and prev_tok == MAX_REPEAT:
                repeat_val_type = type(prev_val[2])
                repeat_val = prev_val[2]
                if repeat_val_type == SubPattern:
                    repeat_val = repeat_val.data

                if len(repeat_val) == 1:
                    if _pair_eq(repeat_val[0], (tok, val)):
                        if prev_val[0] != MAXREPEAT and prev_val[1] != MAXREPEAT:
                            prev_val = prev_val[0] + 1, prev_val[1] + 1, prev_val[2]
                        new[-1] = prev_tok, prev_val
                        continue

            elif tok == MAX_REPEAT and prev_tok == LITERAL:
                repeat_val_type = type(val[2])
                repeat_val = val[2]
                if repeat_val_type == SubPattern:
                    repeat_val = repeat_val.data

                if len(repeat_val) == 1:
                    if _pair_eq(repeat_val[0], (prev_tok, prev_val)):
                        prev_tok = MAX_REPEAT
                        if val[0] != MAXREPEAT and val[1] != MAXREPEAT:
                            prev_val = val[0] + 1, val[1] + 1, val[2]
                        else:
                            prev_val = val[0], val[1], val[2]

                        new[-1] = prev_tok, prev_val
                        continue

            elif tok == MAX_REPEAT:
                val = (val[0], val[1], create_subpattern(_simplify_sre_list(val[2])))

            elif tok == SUBPATTERN:
                val = (*val[0:3], create_subpattern(_simplify_sre_list(val[3])))

        new.append((tok, val))
        prev_tok = tok
        prev_val = val

    return new


def _pair_eq(a, b):
    tok = a[0]
    if tok != b[0]:
        return False

    val_a = a[1]
    val_b = b[1]

    if tok == MAX_REPEAT:
        if val_a[0:2] != val_b[0:2]:
            return False
        return _val_eq(val_a[-1], val_b[-1])

    elif tok == SUBPATTERN:
        if val_a[0:3] != val_b[0:3]:
            return False
        return _val_eq(val_a[-1], val_b[-1])

    return _val_eq(a[1], b[1])


def _val_eq(a, b):
    type_a = type(a)
    type_b = type(b)

    if type_a == SubPattern:
        if type_b == SubPattern:
            b = b.data
            type_b = type(b)

        assert type_b == list
        return _val_eq(a.data, b)
    elif type_b == SubPattern:
        return _val_eq(b, a)

    if type_a != type_b:
        return False

    if type_a in [int, _NamedIntConstant]:
        return a == b

    length = len(a)
    if length != len(b):
        return False

    types_a = list(type(i) for i in a)
    types_b = list(type(i) for i in b)
    if types_a != types_b:
        if types_a[:-1] == types_b[:-1]:
            return _val_eq(a[-1], b[-1])

        return False

    if type_a is list:
        for i, val in enumerate(a):
            if not _val_eq(val, b[i]):
                return False
        return True

    assert type_a == tuple, type_a

    if length == 2:
        tok, val = a
        if tok == MAX_REPEAT:
            return _val_eq(val, b[1])
        elif tok == SUBPATTERN:
            return _pair_eq(a, b)

    elif length == 3:
        if types_a[2] == SubPattern:
            subpattern_a = a[2]
            subpattern_b = b[2]
            return _val_eq(subpattern_a, subpattern_b)

    return a == b
