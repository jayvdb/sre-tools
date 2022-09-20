from __future__ import unicode_literals

import re
import sre_parse
import unittest

from sre_tools.analyse import check_regex


class TestAnalyseRegex(unittest.TestCase):

    def _assert_valid(self, a):
        check_regex(a)

    def _assert_invalid(self, a, msg):
        with self.assertRaisesRegexp(re.error, msg):
            check_regex(a)

    def test_valid_union(self):
        self._assert_valid(r"[\s\S]")

    def test_invalid_union_inverted(self):
        self._assert_invalid(r"[^\s\S]", "cant negate all matches")
