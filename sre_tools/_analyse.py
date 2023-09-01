from sre_parse import (
    CATEGORY,
    CHCODES,
    error,
    IN,
    NEGATE,
)


def _handle_error(tok, val, msg):
    raise error(msg)


def preprocess(seq, error=_handle_error):
    for tok, val in list(seq):
        if tok == IN:
            negate = val[0] == (NEGATE, None)
                    
            cats = sorted(in_cat for in_type, in_cat in val if in_type == CATEGORY)
            for i in range(0, len(CHCODES), 2):
                if CHCODES[i] in cats and CHCODES[i+1] in cats:
                    if negate:
                        _handle_error(tok, val, "cant negate all matches")
                    else:
                        yield tok, val, True
                        break
            else:
                yield tok, val, cats

        else:
            yield tok, val, None
