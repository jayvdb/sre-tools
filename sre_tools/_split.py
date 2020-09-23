import sre_parse

from .utils import create_subpattern


def split_regex(pattern, at, remainer=False):
    if not isinstance(pattern, sre_parse.SubPattern):
        pattern = sre_parse.parse(pattern)
    found = False
    if remainer:
        new = create_subpattern()
    else:
        new = None
    for i, (tok, val) in enumerate(list(pattern.data)):
        if not found and tok == sre_parse.LITERAL and val == ord(at):
            found = True
            del pattern[i]
            continue
        elif not found and tok == sre_parse.IN and (sre_parse.LITERAL, ord(at)) in val:
            found = True
            del pattern[i]
            continue
        elif not found and tok == sre_parse.MAX_REPEAT:
            val = val[2]
            if (sre_parse.LITERAL, ord(at)) in val:
                found = True
                del pattern[i]
                continue
        if found:
            if remainer:
                new.append((tok, val))
            del pattern[-1]
    if not found:
        return pattern, None
    return pattern, new
