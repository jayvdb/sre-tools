from __future__ import unicode_literals

import sre_compile
import sre_parse
import unittest

from sre_tools._simplify import _val_eq
from sre_tools.simplify import simplify_regex


class TestSimplifyRegex(unittest.TestCase):
    def _assert_equal(self, a, b):
        rv = simplify_regex(a)
        self.assertIsInstance(rv, sre_parse.SubPattern)
        sre_compile.compile(rv)
        assert _val_eq(rv, sre_parse.parse(b).data)

    def test_merge_repeat(self):
        self._assert_equal(r"a{1}a{1}", r"a{2}")
        self._assert_equal(r"a{1}a{3}", r"a{4}")
        self._assert_equal(r"a?a{3}", r"a{3,4}")
        self._assert_equal(r"a{3}a?", r"a{3,4}")
        self._assert_equal(r"a{1,2}a{1,3}", r"a{2,5}")

    def test_merge_repeated_literal(self):
        self._assert_equal(r"aa", r"a{2}")

    def test_merge_repeated_dot(self):
        self._assert_equal(r"..", r".{2}")

    def test_merge_repeated_dot_star(self):
        self._assert_equal(r".*.*", r".*")

    def test_merge_repeated_class(self):
        self._assert_equal(r"[a-e][a-e]", r"[a-e]{2}")
        self._assert_equal(r"[^a-e][^a-e]", r"[^a-e]{2}")

    def test_merge_repeated_category(self):
        self._assert_equal(r"\d\d", r"\d{2}")
        self._assert_equal(r"\d+\d+", r"\d{2,}")

    def test_merge_repeated_at(self):
        self._assert_equal(r"^^", r"^^")

    def test_merge_repeated_mixed(self):
        self._assert_equal(r"a{2}a", r"a{3}")
        self._assert_equal(r"aaa", r"a{3}")
        self._assert_equal(r"aa{2}", r"a{3}")

    def test_anchor(self):
        self._assert_equal(r"^aaa", r"^a{3}")

    def test_anchor_not(self):
        self._assert_equal(r"^[^a]aaa", r"^[^a]a{3}")

    def test_subpattern_optional(self):
        self._assert_equal(r"(aa)?", r"(a{2})?")

    def test_subpattern_capture(self):
        self._assert_equal(r"(?:[a-z]{,10}){,1000}", r"(?:[a-z]{,10}){,1000}")

    def test_subpattern_capture_nested(self):
        self._assert_equal(
            r"(?:(?:[a-z]{,100}){,100}){,100}", r"(?:(?:[a-z]{,100}){,100}){,100}"
        )
