from __future__ import unicode_literals

import sre_compile
import sre_parse
import unittest

from sre_parse import LITERAL

from sre_tools._split import split_regex


class TestSplitRegex(unittest.TestCase):
    def test_split_none(self):
        rv = split_regex(r"^ab", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[1] is None

    def test_split_one(self):
        rv = split_regex(r"a/b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        c0 = sre_compile.compile(rv[0])
        assert c0.match("a")
        assert not c0.match("b")
        assert c0.pattern is None

        assert isinstance(rv[1], sre_parse.SubPattern), rv[1].__class__.__name__
        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

        c1 = sre_compile.compile(rv[1])
        assert c1.match("b")
        assert not c1.match("a")
        assert c1.pattern is None

    def test_split_multiple(self):
        rv = split_regex(r"a/b/c", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(LITERAL, ord("a"))]

        c0 = sre_compile.compile(rv[0])
        assert c0.match("a")
        assert not c0.match("b")
        assert c0.pattern is None

        assert isinstance(rv[1], sre_parse.SubPattern), rv[1].__class__.__name__
        assert rv[1].data == [(LITERAL, ord("b")), (LITERAL, 47), (LITERAL, 99)]

        c1 = sre_compile.compile(rv[1])
        assert not c1.match("b")
        assert not c1.match("a")
        assert c1.match("b/c")
        assert c1.pattern is None

    def test_split_at(self):
        rv = split_regex(r"^/b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.AT, sre_parse.AT_BEGINNING)]

        assert isinstance(rv[1], sre_parse.SubPattern), rv[1].__class__.__name__
        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_skip_not(self):
        rv = split_regex(r"[^/]a/b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [
            (sre_parse.NOT_LITERAL, ord("/")),
            (sre_parse.LITERAL, ord("a")),
        ]

        assert isinstance(rv[1], sre_parse.SubPattern), rv[1].__class__.__name__
        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_min_max(self):
        rv = split_regex(r"a/{1,3}b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_plus(self):
        rv = split_regex(r"a/+b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_star(self):
        rv = split_regex(r"a/*b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_class(self):
        rv = split_regex(r"a[/]b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]

    def test_split_class2(self):
        rv = split_regex(r"a[(/]b", "/", remainer=True)
        assert isinstance(rv, tuple), rv
        assert isinstance(rv[0], sre_parse.SubPattern), rv
        assert rv[0].data == [(sre_parse.LITERAL, ord("a"))]

        assert rv[1].data == [(sre_parse.LITERAL, ord("b"))]
